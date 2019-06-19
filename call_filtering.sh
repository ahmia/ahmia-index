#!/bin/bash

# If the environment file does not exist, create it based on example.env
if [ ! -f .env ]; then
    echo "File .env not found, copying from example.env"
    cp example.env .env
fi

# Parse the environment variables from .env file
export $(cat .env | grep -v ^# | xargs)

# We want to filter domains which are in this file
inputfile="filter_these_domains.txt"
inputfile_uniq="filter_these_domains_unique.txt"

torsocks python3 child_abuse_onions.py >> ${inputfile}

sort filter_these_domains.txt | uniq > ${inputfile_uniq}

cp $inputfile_uniq $inputfile

# Read line by line
while read domain; do
    if [ ! -z "$domain" ]; then
        python3 filter_onions.py $domain
        python3 filter_onions.py $domain
    fi
done < ${inputfile_uniq}

# Call elasticsearch cleaning and optimatization
echo "cleaning "
echo "${ES_URL}${ES_TOR_INDEX}/_forcemerge?only_expunge_deletes=true"

curl -XPOST "${ES_URL}${ES_TOR_INDEX}/_forcemerge?only_expunge_deletes=true"
