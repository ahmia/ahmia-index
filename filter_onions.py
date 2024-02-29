# -*- coding: utf-8 -*-
""" Filter some onions from the index """
import sys
from elasticsearch import Elasticsearch, NotFoundError
import settings

def print_error_and_quit():
    """Printing the usage information"""
    print("Filters an onion domain from the index.\n")
    print("Usage: python filter_onions.py some.onion")
    print("Example: python filter_onions.py msydqstlz2kzerdg.onion\n")
    sys.exit()

def filter_content(es, domain):
    """ Bans certain onions """
    try:
        # Query to find documents matching the domain
        query = {
            "size": 30000,
            "query": {
                "bool": {
                    "must": [
                        {"match": {"domain": domain}}
                    ],
                    "must_not": [
                        {"match": {"is_banned": True}}
                    ]
                }
            }
        }
        response = es.search(index=settings.ES_TOR_INDEX, body=query)
        hits = response["hits"]["hits"]
        total = len(hits)
        print(f"Found {total} documents to update.")

        for index, hit in enumerate(hits):
            doc_id = hit['_id']
            index_name = hit['_index']
            print(f"{index+1}/{total} - Updating document ID: {doc_id}")
            # Update document to set is_banned to True
            es.update(index=index_name, id=doc_id, body={"doc": {"is_banned": True}})
            print(f"Document {doc_id} updated.")

        print("Filtered the content.")

    except NotFoundError:
        print("Index not found. Please check the index name.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    """ Read command line arguments """
    if len(sys.argv) != 2 or len(sys.argv[1]) < 22:
        print_error_and_quit()

    domain = sys.argv[1]

    # Connect to Elasticsearch
    es = Elasticsearch(
        [settings.ES_HOST],
        ca_certs=settings.ES_CA_CERTS,
        basic_auth=(settings.ES_USERNAME, settings.ES_PASSWORD)
    )

    filter_content(es, domain)

if __name__ == '__main__':
    main()
