#!/bin/bash

# We want to filter domains which are in this file
inputfile="filter_these_domains.txt"

# Read line by line
while read domain; do
    if [ ! -z "$domain" ]; then
        ./venv3/bin/python filter_onions.py $domain
        ./venv3/bin/python filter_onions.py $domain
    fi
done < $inputfile

# Call elasticsearch cleaning and optimatization
curl -XPOST "http://localhost:9200/crawl/_forcemerge?only_expunge_deletes=true"

