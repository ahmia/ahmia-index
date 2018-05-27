from decouple import config

ES_URL = config('ES_URL', default="http://localhost:9200/")
ES_INDEX = config('ES_INDEX', default="latest-crawl")
