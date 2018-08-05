#!/usr/bin/env python
import argparse
from datetime import datetime, timedelta

import requests

import settings


def _previous_month(dt):
    return datetime(dt.year, dt.month, 1) - timedelta(days=1)


def index_months(months_ago=0):
    month = datetime.now()
    months_removed = 0
    while months_removed != months_ago:
        month = _previous_month(month)
        months_removed = months_removed + 1
    return month.strftime("%Y-%m")


def point_to_new_indexes(to_add=True, to_rm=True):
    """
    Removes the existing alias of latest-tor/i2p to the older linked crawl,
    and makes new latest-tor and i2p aliases to the last two months' crawls.

    :param to_add: If False do not add new aliases
    :param to_rm: If False do not remove old alias
    """

    es_aliases_url = "{}_aliases?pretty".format(settings.ES_URL)
    header = {'Content-Type': 'application/json'}

    if to_rm:
        # remove old aliases
        cmd = {"remove": {"index": "tor-" + index_months(2), "alias": "latest-tor"}}
        actions_json = {"actions": [cmd]}
        resp = requests.post(es_aliases_url, json=actions_json, headers=header)
        print("{0}\n{1}".format(resp.status_code, resp.text))

        cmd = {"remove": {"index": "i2p-" + index_months(2), "alias": "latest-i2p"}}
        actions_json = {"actions": [cmd]}
        resp = requests.post(es_aliases_url, json=actions_json, headers=header)
        print("{0}\n{1}".format(resp.status_code, resp.text))

    if to_add:
        for i in range(0, 1):   # last two months

            # tor
            cmd = {"add": {"index": "tor-" + index_months(i), "alias": "latest-tor"}}
            actions_json = {"actions": [cmd]}
            resp = requests.post(es_aliases_url, json=actions_json, headers=header)
            print("{0}\n{1}".format(resp.status_code, resp.text))

            # i2p
            cmd = {"add": {"index": "i2p-" + index_months(i), "alias": "latest-i2p"}}
            actions_json = {"actions": [cmd]}
            resp = requests.post(es_aliases_url, json=actions_json, headers=header)
            print("{0}\n{1}".format(resp.status_code, resp.text))


def main():
    """
    Define optional parameters to distinguish add & remove procedures
    so that the caller could add only or remove only. At least one of the
    action has to be supplied (aka: True), else both will be executed
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('--add', dest='add', action='store_true', default=False)
    parser.add_argument('--rm', dest='rm', action='store_true', default=False)
    args = parser.parse_args()

    # Update Aliases
    if args.add or args.rm:
        point_to_new_indexes(to_add=args.add, to_rm=args.rm)
    else:
        # If neither add nor rm was specified, do both
        point_to_new_indexes()

    # checkout the new aliases
    resp = requests.get("{}_cat/aliases".format(settings.ES_URL))
    print("new aliases are:\n%s" % resp.content.decode())


if __name__ == '__main__':
    main()
