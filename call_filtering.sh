#!/bin/bash

# We want to filter domains which are in this file
inputfile="filter_these_domains.txt"

# Read line by line
while read domain; do
    if [ ! -z "$domain" ]; then
        python3 filter_onions.py $domain
        python3 filter_onions.py $domain
    fi
done < $inputfile

# Call elasticsearch cleaning and optimatization
curl -XPOST "http://localhost:9200/crawl/_forcemerge?only_expunge_deletes=true"

