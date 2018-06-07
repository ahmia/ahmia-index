#!/usr/bin/env python

from datetime import datetime, timedelta

import requests

# todo improve the project structure ~ currently even relative imports dont work
import settings


def _previous_month(dt):
    return datetime(dt.year, dt.month, 1) - timedelta(days=1)


def _index_months(months_ago=0):
    month = datetime.now()
    months_removed = 0
    while months_removed != months_ago:
        month = _previous_month(month)
        months_removed = months_removed + 1
    return month.strftime("crawl-%Y-%m")


def point_to_new_indexes():
    """ Removes any existing alias of latest-crawl, looking at the indexes that
        correspond to the last 5 months, and creates a new one for the current month
    """

    es_aliases_url = "{}_aliases?pretty".format(settings.ES_URL)
    header = {'Content-Type': 'application/json'}
    actions_json = {"actions": []}

    cmd = {"remove": {"index": _index_months(2), "alias": "latest-crawl"}}
    actions_json["actions"].append(cmd)

    cmd = {"add": {"index": _index_months(1), "alias": "latest-crawl"}}
    actions_json["actions"].append(cmd)

    cmd = {"add": {"index": _index_months(), "alias": "latest-crawl"}}
    actions_json["actions"].append(cmd)

    resp = requests.post(es_aliases_url, json=actions_json, headers=header)
    print("{0}\n{1}".format(resp.status_code, resp.text))


if __name__ == '__main__':
    point_to_new_indexes()
