# Ahmia index

The Ahmia search engine uses Elasticsearch indexes to save website text.

## Installation

* Install Elasticsearch 8
* Install Python3 and pip
* Install the Python packages required, preferably in a virtual environment, with:
```
pip install -r requirements.txt
```

## Configuration

`example.env` contains some default values that should work out of the box.
Copy this to `.env` to create your own instance of environment settings:

```
cp example.env .env
```

Review the `.env` file to ensure that it fits your needs. Make any modifications needed there.


### Elasticsearch

Default configuration is enough to run index in dev mode. Here is suggestion for a more secure configuration

#### /etc/security/limits.conf

```
elasticsearch - nofile unlimited
elasticsearch soft memlock unlimited
elasticsearch hard memlock unlimited
```

#### /etc/default/elasticsearch

```
MAX_OPEN_FILES=unlimited
MAX_LOCKED_MEMORY=unlimited
```

#### /etc/elasticsearch/elasticsearch.yml

```
bootstrap.memory_lock: true
```

#### /etc/elasticsearch/jvm.options

```
-Xms15g
-Xmx15g
```

## Start the service

```sh
sudo systemctl start elasticsearch
```

## Give users permissions to use the HTTPS cert

Any user on the system can read the certificate file,
which is generally acceptable for a public certificate authority (CA) certificate
as it does not contain sensitive private keys.

```sh
sudo mkdir -p /usr/local/share/ca-certificates/
sudo cp /etc/elasticsearch/certs/http_ca.crt /usr/local/share/ca-certificates/
sudo chmod 644 /usr/local/share/ca-certificates/http_ca.crt
```

## Init mappings
Please set mappings running for the first time

```sh
bash setup_index.sh
```

Alternatively, you could set up the indices manually, somehow like this:

```sh
curl -i --cacert /usr/local/share/ca-certificates/http_ca.crt -u elastic -XPUT \
'https://localhost:9200/tor-2024-01/' \
-H 'Content-Type: application/json' -d "@./mappings_tor.json"
```

## Keep `latest-tor` aliase pointed to latest monthly indices
This needs to be the first time you deploy and then once per month

```sh
python point_to_indexes.py
```

## Filter some abuse sites

```sh
bash call_filtering.sh
```

## Crontab

```sh
# Execute child abuse text filtering over the index every hour
30 * * * * cd /home/juha/ahmia-index && bash wrap_filtering.sh > ./crontab_filter.log 2>&1
# First of Each Month:
10 04 01 * * cd /home/juha/ahmia-index && python point_to_indexes.py --add > ./add_alias.log 2>&1
# On 6th of Each Month
10 04 06 * * cd /home/juha/ahmia-index && python point_to_indexes.py --rm > ./remove_alias.log 2>&1
```

## Keep Elasticsearch running: autorestart

```sh
sudo apt install restartd

# Add the following line to /etc/restartd.conf
elasticsearch "elasticsearch" "echo 'Elasticsearch is not running!' >>/tmp/restartd_restart.out && service elasticsearch restart >> /tmp/restartd_restart.out" "echo 'Elasticsearch is running!' >/tmp/restartd.out"

sudo service restartd restart
```
