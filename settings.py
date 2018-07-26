from decouple import config

# The Base URL where Elasticsearch is deployed
ES_URL = config('ES_URL', default="http://localhost:9200/")

# *** ELASTICSEARCH INDICES/ALIASES. These must MATCH the values defined in ahmia-site ***

# The current ES index/alias that holds the onions.
ES_TOR_INDEX = config('ES_TOR_INDEX', default="latest-tor")

# The current ES index/alias that holds the i2p addresses.
ES_I2P_INDEX = config('ES_I2P_INDEX', default="latest-i2p")

# The current index/alias that holds both the onions and i2p addresses
# ES_BOTH_INDEX = config('ES_BOTH_INDEX', default="latest-crawl")   # Currently UNUSED

# todo improve the project structure ~ currently even relative imports dont work
