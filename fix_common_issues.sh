#!/bin/bash

### 0. Parse settings ###

# If the environment file does not exist, create it based on example.env
if [ ! -f .env ]; then
    echo "Warning: File .env not found, copying from example.env"
    cp example.env .env
fi
# Parse the environment variables from .env file, ignoring the comments
export $(cat .env | grep -v ^# | xargs)


### Problem 1: ###
# sometimes, e.g during re-indexing, or low disk space, indices are switched to read-only, undo it
for YEAR in 2018
do
  for MONTH in 01 02 03 04 05 06 07 08 09 10 11 12
  do
     # tor
     curl -XPUT "${ES_URL}tor-$YEAR-$MONTH/_settings" --data '{"index": {"blocks": {"read_only": "false"}}}' -H 'Content-Type: application/json'
     curl -XPUT "${ES_URL}tor-$YEAR-$MONTH/_settings" --data '{"index": {"blocks": {"read_only_allow_delete": "false"}}}' -H 'Content-Type: application/json'

     # i2p
     curl -XPUT "${ES_URL}i2p-$YEAR-$MONTH/_settings" --data '{"index": {"blocks": {"read_only": "false"}}}' -H 'Content-Type: application/json'
     curl -XPUT "${ES_URL}i2p-$YEAR-$MONTH/_settings" --data '{"index": {"blocks": {"read_only_allow_delete": "false"}}}' -H 'Content-Type: application/json'
  done
done