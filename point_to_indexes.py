# -*- coding: utf-8 -*-
""" Point latest-tor to fresh montly indexes """
import argparse
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
import settings

def _previous_month(dt):
    return datetime(dt.year, dt.month, 1) - timedelta(days=1)

def index_months(months_ago=0):
    month = datetime.now()
    months_removed = 0
    while months_removed < months_ago:
        month = _previous_month(month)
        months_removed += 1
    return month.strftime("tor-%Y-%m")

def point_to_new_indexes(es, to_add=True, to_rm=True):
    """
    Update 'latest-tor' alias to point to the latest monthly indexes.
    """

    if to_rm:  # remove old aliases
        try:
            es.indices.update_aliases(body={  # Use 'body' keyword argument
                "actions": [
                    {"remove": {"index": index_months(2), "alias": "latest-tor"}}
                ]
            })
            print(f"Removed alias for {index_months(2)}")
        except Exception as e:
            print(f"Error removing alias: {e}")

    if to_add:
        for i in range(2):  # last two months
            try:
                es.indices.update_aliases(body={  # Use 'body' keyword argument
                    "actions": [
                        {"add": {"index": index_months(i), "alias": "latest-tor"}}
                    ]
                })
                print(f"Added alias for {index_months(i)}")
            except Exception as e:
                print(f"Error adding alias: {e}")

def main():
    """
    Process command-line arguments and update Elasticsearch aliases.
    """

    parser = argparse.ArgumentParser(description='Manage Elasticsearch aliases for the latest-tor index.')
    parser.add_argument('--add', help='Add new aliases', action='store_true')
    parser.add_argument('--rm', help='Remove old aliases', action='store_true')

    args = parser.parse_args()

    # Connect to Elasticsearch
    es = Elasticsearch(
        [settings.ES_HOST],
        ca_certs=settings.ES_CA_CERTS,
        basic_auth=(settings.ES_USERNAME, settings.ES_PASSWORD)
    )

    # Update Aliases
    if args.add or args.rm:
        point_to_new_indexes(es, to_add=args.add, to_rm=args.rm)
    else:
        # Default to updating aliases if no specific action is specified
        point_to_new_indexes(es)

    # Checkout the new aliases
    try:
        resp = es.cat.aliases()
        print("New aliases are:\n", resp)
    except Exception as e:
        print(f"Error fetching aliases: {e}")

if __name__ == '__main__':
    main()
