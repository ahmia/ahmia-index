#!/bin/bash

for YEAR in 2018 2019
do
  for MONTH in 01 02 03 04 05 06 07 08 09 10 11 12
  do
    curl -XPUT -i "localhost:9200/crawl-$YEAR-$MONTH/" -H 'Content-Type: application/json' -d "@./mappings.json"
  done
done
