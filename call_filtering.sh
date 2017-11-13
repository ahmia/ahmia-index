#!/bin/bash

# We want to filter domains which are in this file
inputfile_uniq="filter_these_domains_unique.txt"

torsocks python child_abuse_onions.py >> filter_these_domains.txt

sort filter_these_domains.txt | uniq > $inputfile_uniq

# Read line by line
while read domain; do
    if [ ! -z "$domain" ]; then
        ./venv3/bin/python filter_onions.py $domain
        ./venv3/bin/python filter_onions.py $domain
    fi
done < $inputfile_uniq

# Call elasticsearch cleaning and optimatization
curl -XPOST "http://localhost:9200/latest-crawl/_forcemerge?only_expunge_deletes=true"

