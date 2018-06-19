""" The purpose of this script to is to help migrate elasticsearch data stored in crawl-yyyy-mm
    to new indices: tor-yyyy-mm and i2p-yyyy-mm, for the last two months' crawls

    __NOTE__: Run this script only ONCE, else will create duplicate information. In that
              case you could recreate the index and rerun
"""
import json
from urllib.parse import urljoin

import requests

import settings
from point_to_indexes import index_months


def _print_results(response):
    """ display the resulting stats from the transfer """
    if isinstance(response, bytes):
        response = response.decode('utf-8')

    pydict = json.loads(response)
    print("took: {0}\ntotal: {1}\ncreated: {2}\nupdated: {3}\n".format(
        pydict.get('took'),
        pydict.get('total'),
        pydict.get('created'),
        pydict.get('updated'),
        pydict.get('deleted'))
    )


endpoint = urljoin(settings.ES_URL, "_reindex/")
print(endpoint)

for i in range(0, 2):
    """ for the last 2 months migrate data to new indices """

    # copy crawl-yyyy-mm index data of mapping type 'tor' to tor-yyyy-mm
    payload = {
      "source": {
        "index": "crawl-%s" % index_months(i),
        "type": "tor"
      },
      "dest": {
        "index": "tor-%s" % index_months(i),
        "type": "doc"
      }
    }
    r = requests.post(endpoint, json=payload)
    _print_results(r.content)

    # copy crawl-yyyy-mm index data of mapping type 'i2p' to i2p-yyyy-mm
    payload['source']['type'] = 'i2p'
    payload['dest']['index'] = "i2p-%s" % index_months(i)
    r = requests.post(endpoint, json=payload)
    _print_results(r.content)


