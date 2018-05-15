import requests
from datetime import datetime, timedelta  # Index name according to YEAR-MONTH


def previous_month(dt):
    return datetime(dt.year, dt.month, 1) - timedelta(days=1)


def index_months(months_ago=0):
    month = datetime.now()
    months_removed = 0
    while months_removed != months_ago:
        month = previous_month(month)
        months_removed = months_removed + 1
    return month.strftime("crawl-%Y-%m")


def point_to_new_indexes():
    es_url = "http://localhost:9200/_aliases?pretty"
    actions_json = {
        "actions": []
    }

    for i in (2, 1, 0):
        cmd = {
            "remove": {
                "index": index_months(i),
                "alias": "latest-crawl"
            }
        }
        actions_json["actions"].append(cmd)

    header = {
        'Content-Type': 'application/json'
    }
    resp = requests.post(es_url, json=actions_json, headers=header)
    print(resp.status_code)
    print(resp.text)


if __name__ == '__main__':
    point_to_new_indexes()
