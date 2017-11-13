# -*- coding: utf-8 -*-
""" Filter some onions from the index """

import sys
import requests

def printErrorAndQuit():
    """Printing the usage information"""
    print("Filters an onion domain from the index.\n")
    print("Usage: python3 filter_onions.py some.onion")
    print("Example: python3 filter_onions.py msydqstlz2kzerdg.onion\n")
    sys.exit()

def main():
    # Read command line arguments
    try:
        if len(sys.argv) == 2:
            domain = str(sys.argv[1])
            if len(domain) == 22:
                filterContent(domain)
            else:
                printErrorAndQuit()
        else:
            printErrorAndQuit()
    except Exception as e:
        print( str(e) )
        printErrorAndQuit()

def filterContent(domain):
    """ Bans certain onions """
    INDEX_NAME = "latest-crawl"
    ES = "http://localhost:9200/"
    url = ES + INDEX_NAME # URL of the new index
    print('\033[1;30m Test that Elasticsearch is available: %s \033[1;m' % url)
    try:
        r = requests.head(url)
    except requests.exceptions.RequestException as e:
        print(e)
        print('\033[1;31m Cannot connect to Elasticsearch (%s)! \033[1;m' % url)
        sys.exit()
    print('\033[1;32m ---> Yes, Elasticsearch is available!\033[1;m')
    query = url + '/tor/_search?pretty&size=1000&q=domain:"' + domain + '"'
    query = query + " AND NOT is_banned:1"
    r = requests.get(query)
    if r.status_code == 200:
        hits = r.json()["hits"]["hits"]
        total = len(hits)
        if total > 0:
            for index, hit in enumerate(hits):
                if hit['_source']['domain'] == domain:
                    target_url = hit['_source']['url']
                    result = "%d/%d Filtering %s" % (index+1, total, target_url)
                    print('\033[1;30m ' + result + ' \033[1;m')
                    if index > 0:
                        query = ES + hit["_index"] + '/tor/' + hit['_id']
                        r = requests.delete(query)
                    else:
                        json_data = { "doc" : { "is_banned": 1 } }
                        query = ES + hit["_index"] + '/tor/' + hit['_id'] + '/_update'
                        r = requests.post(query, json=json_data)
        else:
            print('\033[1;31m No search results! \033[1;m')
    else:
        print('\033[1;31m Search failed! \033[1;m')
    print('\033[1;32m Filtered the content. \033[1;m')
    print('\033[1;32m You can run this again to remove sites. \033[1;m')

if __name__ == '__main__':
    main()
