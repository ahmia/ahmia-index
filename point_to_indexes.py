#!/usr/bin/env python

from datetime import datetime, timedelta

import requests

# todo improve the project structure ~ currently even relative imports dont work
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


def point_to_new_indexes():
    """ Removes the existing alias of latest-tor/i2p to the older linked crawl, and make new
        latest-tor/i2p aliases with the last two months' crawls. Thus we should have
        2 tor-latest aliases and 2 i2p-latest aliases
    """

    es_aliases_url = "{}_aliases?pretty".format(settings.ES_URL)
    header = {'Content-Type': 'application/json'}
    actions_json = {"actions": []}

    cmd = {"remove": {"index": "tor-" + index_months(2), "alias": "latest-tor"}}
    actions_json["actions"].append(cmd)

    cmd = {"add": {"index": "tor-" + index_months(1), "alias": "latest-tor"}}
    actions_json["actions"].append(cmd)

    cmd = {"add": {"index": "tor-" + index_months(), "alias": "latest-tor"}}
    actions_json["actions"].append(cmd)

    cmd = {"remove": {"index": "i2p-" + index_months(2), "alias": "latest-i2p"}}
    actions_json["actions"].append(cmd)

    cmd = {"add": {"index": "i2p-" + index_months(1), "alias": "latest-i2p"}}
    actions_json["actions"].append(cmd)

    cmd = {"add": {"index": "i2p-" + index_months(), "alias": "latest-i2p"}}
    actions_json["actions"].append(cmd)

    # todo add latest-crawl to all of the above, to have a common alias for both tor & i2p crawls?

    resp = requests.post(es_aliases_url, json=actions_json, headers=header)
    print("{0}\n{1}".format(resp.status_code, resp.text))


if __name__ == '__main__':
    point_to_new_indexes()
