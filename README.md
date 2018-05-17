# Ahmia index
Ahmia search engine use elasticsearch to index content.

## Installation
* Please install elastic search 5.x from the official repository thanks to the [official guide](https://www.elastic.co/guide/en/elastic-stack/5.6/elastic-stack.html)
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
Default configuration is enough to run index in dev mode. Here is suggestion for a more secure configuration

### /etc/security/limits.conf

```
elasticsearch - nofile unlimited
elasticsearch - memlock unlimited
```

### /etc/default/elasticsearch
on CentOS/RH: /etc/sysconfig/elasticsearch

```
ES_HEAP_SIZE=2g # Half of your memory, other half is for Lucene
MAX_OPEN_FILES=1065535
MAX_LOCKED_MEMORY=unlimited
```

### /etc/elasticsearch/elasticsearch.yml

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
$ curl -XPUT -i "localhost:9200/crawl-2017-10/" -H 'Content-Type: application/json' -d "@./mappings.json"
$ curl -XPUT -i "localhost:9200/crawl-2017-11/" -H 'Content-Type: application/json' -d "@./mappings.json"
$ curl -XPUT -i "localhost:9200/crawl-2017-12/" -H 'Content-Type: application/json' -d "@./mappings.json"
```

or

```sh
$ bash setup_index.sh
```

## Keep latest-crawl pointed to latest monthly indexes

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
