# Ahmia index
Ahmia search engine uses Elasticsearch 2.4 or 5.4.3 to index content.

## Installation
Please install elastic search from the official repository. Elasticsearch 2.4 and 5.x both work.

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
ES_HEAP_SIZE=3g # For ES 2.4! Half of your memory, other half is for Lucene
MAX_OPEN_FILES=1065535
MAX_LOCKED_MEMORY=unlimited
```

### For ES 5.4.3 /etc/elasticsearch/jvm.options
```
# For ES 5.4.3! Half of your memory, other half is for Lucene
-Xms3g
-Xmx3g
```


### /etc/elasticsearch/elasticsearch.yml

```
bootstrap.mlockall: true # For ES 2.4!
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
# If ES 5.x
$ curl -XPUT "localhost:9200/_cluster/settings" -d '{
    "transient" : {
        "script.max_compilations_per_minute" : 200
    }
}'
```
## Crontab for Auto Blacklisting of Child Abuse Websites (torsocks required)
```
0 22 * * * cd /your/ahmia/folder/ && torsocks python child_abuse_onions.py > filter_these_domains.txt && bash call_filtering.sh

```
