#!/bin/bash

# If the environment file does not exist, create it based on example.env
if [ ! -f .env ]; then
    echo "Warning: File .env not found, copying from example.env"
    cp example.env .env
fi

# Parse the environment variables from .env file, ignoring the comments
export $(cat .env | grep -v ^# | xargs)

for YEAR in {2018..2030}; do
  for MONTH in 01 02 03 04 05 06 07 08 09 10 11 12; do
    
    curl --cacert ${ES_CA_CERTS} --user ${ES_USERNAME}:${ES_PASSWORD} \
    -XPUT "${ES_URL}$YEAR-$MONTH/" \
    -H 'Content-Type: application/json' -d "@./mappings_tor.json"

    echo ""
  done
done
