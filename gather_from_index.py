# -*- coding: utf-8 -*-
""" Filter websites based on keywords """
from elasticsearch import Elasticsearch
import settings  # Import the settings from settings.py

ALLOWED_DOMAINS = [
    "donionsixbjtiohce24abfgsffo2l4tk26qx464zylumgejukfq2vead.onion",
    "deeeepv4bfndyatwkdzeciebqcwwlvgqa6mofdtsvwpon4elfut7lfqd.onion",
    "juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion"
]

def search(es, domain_list, keywords_list):
    """
    Search domains for filtering.
    """
    query = {
        "size": 30000,
        "_source": ["title", "domain"],
        "query": {
            "bool": {
                "should": [
                    {"match_phrase": {"content": keyword}} for keyword in keywords_list
                ]
            }
        }
    }
    resp = es.options(request_timeout=90).search(index=settings.ES_TOR_INDEX, body=query)
    hits = resp['hits']['hits']
    for hit in hits:
        domain = hit.get("_source", {}).get("domain", "")
        if domain and domain not in domain_list and domain not in ALLOWED_DOMAINS:
            print(domain)
            domain_list.append(domain)

def main():
    """
    Search based on keywords and filter pages.
    """
    # Use the imported settings
    es = Elasticsearch(
        [settings.ES_HOST],
        ca_certs=settings.ES_CA_CERTS,
        basic_auth=(settings.ES_USERNAME, settings.ES_PASSWORD)
    )

    domain_list = []
    keywords_list = ['preteen', 'loli', 'lolita', 'jailbait', 'pthc', 'best cp',
                     'child porn', 'kid porn', 'child sex', 'cp video',
                     'nude children', 'cp porn', 'free child porn', 'kinderporn',
                     'child rape', 'toddler porn', 'kids videos', 'cp videos',
                     'lolilust', 'pedo porno', 'pedo content', 'underage', 'cp pack',
                     'loliporn', 'pedofamily', 'cp database', 'pedo webcams', 'lolitacity',
                     'xxx child', 'xxx underage', 'young forbidden']

    search(es, domain_list, keywords_list)

if __name__ == '__main__':
    main()
