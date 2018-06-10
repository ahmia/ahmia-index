# Ahmia index
Ahmia search engine use elasticsearch to index content.

## Installation
* Please install elastic search 6.2+ from the official repository thanks to the [official guide](https://www.elastic.co/guide/en/elastic-stack/6.2/elastic-stack.html)
* Install *python3, python3-pip*.
* Install python packages required, preferably in a virtualenv, with:
```
pip install -r requirements.txt
```

Ensure that you default version is python3:
```
python --version
```

## Configuration

`example.env` contains some default values that should work out of the box. Copy this to `.env` to create
your own instance of environment settings:

```
cp example.env .env
```

Review the `.env` file to ensure that it fits your needs. Make any modifications needed there.


### Elasticsearch

Default configuration is enough to run index in dev mode. Here is suggestion for a more secure configuration

#### /etc/security/limits.conf

```
elasticsearch - nofile unlimited
elasticsearch - memlock unlimited
```

#### /etc/default/elasticsearch
on CentOS/RH: /etc/sysconfig/elasticsearch

```
ES_HEAP_SIZE=2g # Half of your memory, other half is for Lucene
MAX_OPEN_FILES=1065535
MAX_LOCKED_MEMORY=unlimited
```

#### /etc/elasticsearch/elasticsearch.yml

```
bootstrap.mlockall: true
script.engine.groovy.inline.update: on
script.engine.groovy.inline.aggs: on
```

## Start the service

```sh
# systemctl start elasticsearch
```

```sh
curl -XPUT 'http://localhost:9200/_all/_settings?preserve_existing=true' -d '{
  "index.max_result_window" : "30000"
}'
```

## Init mappings
Please do this when running for the first time

```sh
$ bash setup_index.sh
```

Alternatively you could set up the indices manually, somehow like this:

```sh
$ curl -XPUT -i "localhost:9200/tor-2018-01/" -H 'Content-Type: application/json' -d "@./mappings_tor.json"
$ curl -XPUT -i "localhost:9200/i2p-2018-01/" -H 'Content-Type: application/json' -d "@./mappings_i2p.json"
$ curl -XPUT -i "localhost:9200/tor-2018-02/" -H 'Content-Type: application/json' -d "@./mappings_tor.json"
$ curl -XPUT -i "localhost:9200/i2p-2018-02/" -H 'Content-Type: application/json' -d "@./mappings_i2p.json"
...
...
```

## Keep `latest-tor`, `latest-i2p` aliases pointed to latest monthly indices
This needs to be the first time you deploy and then once per month

```sh
$ python point_to_indexes.py
```

## Filter some abuse sites

```sh
$ bash call_filtering.sh
```

## Crontab

```sh
# Every day
50 09 * * * cd /usr/local/home/juha/ahmia-index && bash call_filtering.sh > ./filter.log 2>&1
# Once a month
10 04 16 * * cd /usr/local/home/juha/ahmia-index && python point_to_indexes.py > ./change_alias.log 2>&1
```
