#!/bin/bash
# Start filtering script if it is not already running

pgrep -f call_filtering.sh

if [ $? -eq 0 ] # Already running
then
    exit
fi

# Else start the script
bash call_filtering.sh > ./filter.log 2>&1
