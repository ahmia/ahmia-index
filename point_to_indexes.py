import requests
from datetime import datetime, timedelta # Index name according to YEAR-MONTH

def index_months(months_ago=0):
    month = datetime.now()
    months_removed = 0
    while months_removed != months_ago:
        month = previous_month(month)
        months_removed = months_removed + 1
    return month.strftime("crawl-%Y-%m")

def previous_month(dt):
   return datetime(dt.year, dt.month, 1) - timedelta(days=1)

def point_to_new_indexes():
    es_connection = "http://localhost:9200/"
    actions_json = {"actions":[]}

    cmd = { "remove" : { "index" : index_months(2), "alias" : "latest-crawl" } }
    actions_json["actions"].append(cmd)

    cmd = { "add" : { "index" : index_months(1), "alias" : "latest-crawl" } }
    actions_json["actions"].append(cmd)

    cmd = { "add" : { "index" : index_months(), "alias" : "latest-crawl" } }
    actions_json["actions"].append(cmd)

    requests.post(es_connection+"_aliases?pretty", data=actions_json)

if __name__ == '__main__':
   point_to_new_indexes()
