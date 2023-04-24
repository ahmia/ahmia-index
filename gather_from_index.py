""" Filter websites based on keywords """
import requests

ALLOWED_DOMAINS = ["donionsixbjtiohce24abfgsffo2l4tk26qx464zylumgejukfq2vead.onion",
                   "deeeepv4bfndyatwkdzeciebqcwwlvgqa6mofdtsvwpon4elfut7lfqd.onion",
                   "juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion"]

def search(url, domain_list):
    """
    Search domains for filtering.
    """
    resp = requests.get(url)
    if not resp.json().get('hits', '').get('hits', []):
        return
    for hit in resp.json()["hits"]["hits"]:
        domain = hit.get("_source", {}).get("domain", "")
        if not domain:
            continue
        if not domain in domain_list:
            domain_list.append(domain)
        #print(hit["_source"].get("title", "").encode("ascii","ignore"))
        if domain not in ALLOWED_DOMAINS:
            print(domain)

def main():
    """
    Search based on key words and filter pages.
    """
    domain_list = []
    base_url = "http://localhost:9200/latest-tor/_search?pretty&size=9000&_source=title,domain"
    keywords_list = ['preteen', 'loli', 'lolita', 'jailbait', 'pthc', 'best cp',
                     '"child porn"', '"kid porn"', '"child sex"', '"cp video"',
                     '"nude children"', '"cp porn"', '"free child porn"', 'kinderporn',
                     '"child rape"', '"toddler porn"', '"kids videos"', '"cp videos"',
                     'lolilust', '"pedo porno"', '"pedo content"', 'underage', '"cp pack"',
                     'loliporn', 'pedofamily', '"cp database"', '"pedo webcams"', 'lolitacity']
                     '"xxx child"', '"xxx underage"', '"young forbidden"']
    search_terms = []
    for index, term in enumerate(keywords_list):
        search_terms.append(term)
        if len(search_terms) >= 10 or index + 1 == len(keywords_list):
            url = base_url + "&q=(" + " OR ".join(search_terms).replace(" ", "%20") + ")"
            search(url, domain_list)
            search_terms = []

if __name__ == '__main__':
    main()
