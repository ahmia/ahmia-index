from decouple import config

# The Base URL where Elasticsearch is deployed
ES_HOST = config('ES_URL', default="https://localhost:9200/")

# The current ES index/alias that holds the onions.
ES_TOR_INDEX = config('ES_TOR_INDEX', default="latest-tor")

ES_CA_CERTS = config('ES_CA_CERTS', default='/etc/elasticsearch/certs/http_ca.crt')
ES_USERNAME = config('ES_USERNAME', default='elastic')
ES_PASSWORD = config('ES_PASSWORD', default='password12345')
