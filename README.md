# Ahmia index
Ahmia search engine use elasticsearch to index content.

## Installation
Please install elastic search from the official repository thanks to the [official guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/setup-repositories.html)

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

## Init mappings
Please do this when running for the first time

```sh
$ curl -XPUT -i "localhost:9200/crawl/" -d "@./mappings.json"
```

Index rotation is possible
--------------------------

- This is just an example
- Crawl to the crawl-YEAR-MONTH index
- Point latest-crawl to the latests indexes

```sh
curl -XPOST 'http://localhost:9200/_aliases' -d '
{
    "actions" : [
        { "remove" : { "index" : "crawl-2017-10", "alias" : "latest-crawl" } },
        { "add" : { "index" : "crawl-2017-11", "alias" : "latest-crawl" } },
        { "add" : { "index" : "crawl-2017-12", "alias" : "latest-crawl" } }
    ]
}'
```
