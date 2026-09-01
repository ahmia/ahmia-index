"""
重複サイト検出バッチ処理
========================================
ES全件のsimhashフィールドを使って近似重複グループを検出し、
各ドキュメントに以下のフィールドを書き戻す:

  - duplicate_group_id: 同じ重複グループに属するドキュメントで共通のID
                         （重複がない場合は null）
  - is_representative:  検索結果に表示すべき代表ドキュメントなら true

アルゴリズム:
  1. 全件のsimhash値を取得
  2. ハミング距離 <= K_THRESHOLD のペアをUnion-Findで大まかにグループ化
  3. 各候補グループ内で完全連結クラスタリングを行い、
     「グループ内の最大距離 <= K_THRESHOLD」を保証する形に分割し直す
     （Union-Findだけだと"連鎖"により無関係なサイトが混入するため）
  4. 各グループ内で代表ドキュメント（最終クロール日時が新しいもの）を選ぶ
  5. ESへ一括反映

実行方法（例）:
  python3 build_duplicate_groups.py

定期実行を想定しており、既存のフィルタリングバッチと同様の
crontab運用に組み込むことを想定している。
"""

import time
import uuid
import logging
from collections import defaultdict
from itertools import combinations

import numpy as np
from elasticsearch import Elasticsearch, helpers
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


# ==========================
# 設定パラメータ
# ==========================

INDEX_NAME = "onions-2026-08"
K_THRESHOLD = 1          # ハミング距離の閾値（実データ検証によりk=1を採用）
MAX_RECLUSTER_SIZE = 800  # これを超える候補グループは計算コスト回避のため分割をスキップ

ES_HOST = "https://localhost:9200"
ES_USER = "elastic"
ES_PASSWORD = "8d_g_J6=fBhej3LVFFlE"


es = Elasticsearch(
    ES_HOST,
    basic_auth=(ES_USER, ES_PASSWORD),
    verify_certs=False,
    request_timeout=60,
    max_retries=3,
    retry_on_timeout=True,
)


# ==========================
# ① 全件のsimhash値を取得
# ==========================

def fetch_all_simhashes():
    """
    ESから (doc_id, url, simhash値, updated_on) を全件取得する。
    simhashが存在しないドキュメントはスキップする。
    """
    docs = []
    skipped = 0

    scan = helpers.scan(
        client=es,
        index=INDEX_NAME,
        query={"query": {"exists": {"field": "simhash"}}},
        _source=["url", "simhash", "updated_on"],
        scroll="30m",
    )

    for hit in scan:
        source = hit["_source"]
        simhash_str = source.get("simhash")
        if not simhash_str:
            skipped += 1
            continue
        try:
            simhash_val = int(simhash_str)
        except (TypeError, ValueError):
            skipped += 1
            continue

        docs.append({
            "doc_id": hit["_id"],
            "url": source.get("url", ""),
            "simhash": simhash_val,
            "updated_on": source.get("updated_on", ""),
        })

    logger.info(f"取得件数: {len(docs)}件（simhash欠損でスキップ: {skipped}件）")
    return docs


# ==========================
# ② ハミング距離k以下の候補ペアを高速に列挙
# ==========================

def find_candidate_pairs(docs, k=K_THRESHOLD):
    """
    numpyでベクトル化して、全ペアの中からハミング距離<=kのものだけを抽出する。
    件数が数万件規模までは現実的な速度で計算できる。
    より大規模になった場合は、simhashライブラリのSimhashIndex
    （ブロック分割による近似探索）への切り替えを検討すること。
    """
    n = len(docs)
    hashes = np.array([d["simhash"] for d in docs], dtype=np.uint64)

    pairs = []
    for i in range(n - 1):
        xor = hashes[i] ^ hashes[i + 1:]
        dist = np.bitwise_count(xor)
        matched = np.where(dist <= k)[0]
        for m in matched:
            j = i + 1 + int(m)
            pairs.append((i, j, int(dist[m])))

    logger.info(f"候補ペア数（距離<={k}）: {len(pairs)}")
    return pairs


# ==========================
# ③ Union-Find + 完全連結クラスタリング
# ==========================

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx != ry:
            self.parent[ry] = rx


def hamming(a, b):
    return bin(a ^ b).count("1")


def recluster(indices, docs, k):
    """
    候補グループ内で完全連結クラスタリングを行い、
    「グループ内の最大ペア距離 <= k」を保証したサブグループに分割する。
    Union-Findだけでは、連鎖（A-B, B-Cが近いだけでA-Cは遠い）により
    無関係なサイトが同一グループに混入することがあるため必須の処理。
    """
    n = len(indices)
    if n <= 2:
        return [indices]
    if n > MAX_RECLUSTER_SIZE:
        logger.warning(f"候補グループが大きすぎるため再分割をスキップ（サイズ={n}）")
        return [indices]

    dist_matrix = np.zeros((n, n))
    for a, b in combinations(range(n), 2):
        d = hamming(docs[indices[a]]["simhash"], docs[indices[b]]["simhash"])
        dist_matrix[a, b] = d
        dist_matrix[b, a] = d

    condensed = squareform(dist_matrix, checks=False)
    Z = linkage(condensed, method="complete")
    labels = fcluster(Z, t=k, criterion="distance")

    subgroups = defaultdict(list)
    for local_idx, label in enumerate(labels):
        subgroups[label].append(indices[local_idx])

    return list(subgroups.values())


def build_final_groups(docs, pairs, k=K_THRESHOLD):
    n = len(docs)
    uf = UnionFind(n)
    for i, j, dist in pairs:
        uf.union(i, j)

    candidate_groups = defaultdict(list)
    for idx in range(n):
        candidate_groups[uf.find(idx)].append(idx)

    final_groups = []
    for root, indices in candidate_groups.items():
        if len(indices) < 2:
            continue
        subgroups = recluster(indices, docs, k)
        for sg in subgroups:
            if len(sg) >= 2:
                final_groups.append(sg)

    logger.info(f"最終グループ数: {len(final_groups)}")
    return final_groups


# ==========================
# ④ 代表ドキュメントの選定
# ==========================

def pick_representative(group_indices, docs):
    """
    グループ内で検索結果に表示する代表を選ぶ。
    基準: ① 最終クロール成功日時（updated_on）が新しいもの
          ② 同日時ならURLが短い（シンプルな）もの
    """
    candidates = [docs[i] for i in group_indices]
    candidates.sort(key=lambda d: (d["updated_on"], -len(d["url"])), reverse=True)
    return candidates[0]["doc_id"]


# ==========================
# ⑤ ESへ書き戻す
# ==========================

def flush(actions, failed_log):
    if not actions:
        return
    success, errors = helpers.bulk(es, actions, stats_only=False, raise_on_error=False)
    if errors:
        for err in errors:
            failed_log.append(err)
            logger.error(f"更新失敗: {err}")


def write_back_groups(docs, final_groups):
    """
    各ドキュメントに duplicate_group_id と is_representative を書き込む。
    まず全ドキュメントの値をリセットしてから、重複グループに属するものだけ更新する。
    """
    actions = []
    failed_log = []
    count = 0

    # 重複グループに属さないドキュメントは null にリセットする
    grouped_doc_ids = set()
    for group in final_groups:
        for idx in group:
            grouped_doc_ids.add(docs[idx]["doc_id"])

    for doc in docs:
        if doc["doc_id"] in grouped_doc_ids:
            continue
        actions.append({
            "_op_type": "update",
            "_index": INDEX_NAME,
            "_id": doc["doc_id"],
            "doc": {
                "duplicate_group_id": None,
                "is_representative": True,  # 重複がないので自分自身が代表
            },
        })
        count += 1
        if len(actions) >= 200:
            flush(actions, failed_log)
            actions = []

    # 重複グループに属するドキュメントを更新
    for group in final_groups:
        group_id = str(uuid.uuid4())
        representative_id = pick_representative(group, docs)

        for idx in group:
            doc = docs[idx]
            actions.append({
                "_op_type": "update",
                "_index": INDEX_NAME,
                "_id": doc["doc_id"],
                "doc": {
                    "duplicate_group_id": group_id,
                    "is_representative": (doc["doc_id"] == representative_id),
                },
            })
            count += 1
            if len(actions) >= 200:
                flush(actions, failed_log)
                actions = []

    if actions:
        flush(actions, failed_log)

    logger.info(f"更新試行件数: {count}件, 失敗: {len(failed_log)}件")
    return failed_log


# ==========================
# メイン処理
# ==========================

def main():
    start = time.time()

    docs = fetch_all_simhashes()
    if not docs:
        logger.warning("対象ドキュメントがありません。処理を終了します。")
        return

    pairs = find_candidate_pairs(docs, k=K_THRESHOLD)
    final_groups = build_final_groups(docs, pairs, k=K_THRESHOLD)

    total_dup_sites = sum(len(g) for g in final_groups)
    logger.info(
        f"重複グループ数={len(final_groups)}, "
        f"重複サイト数={total_dup_sites}, "
        f"重複率={total_dup_sites/len(docs)*100:.2f}%"
    )

    failed_log = write_back_groups(docs, final_groups)

    logger.info(f"完了（{time.time()-start:.1f}秒）")
    if failed_log:
        logger.warning(f"一部更新に失敗しています。詳細は上記ログを確認してください（{len(failed_log)}件）")


if __name__ == "__main__":
    main()