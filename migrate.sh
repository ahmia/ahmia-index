#!/bin/bash

# If the environment file does not exist, create it based on example.env
if [ ! -f .env ]; then
    echo "Warning: File .env not found, copying from example.env"
    cp example.env .env
fi

# Parse the environment variables from .env file, ignoring the comments
export $(cat .env | grep -v ^# | xargs)

curl --cacert ${ES_CA_CERTS} --user ${ES_USERNAME}:${ES_PASSWORD} \
-XPUT "${ES_URL}_ingest/pipeline/convert_boolean" \
-H 'Content-Type: application/json' -d'
{
  "description" : "Converts numeric booleans to true or false",
  "processors" : [
    {
      "script": {
        "source": "if (ctx.is_fake != null) { ctx.is_fake = ctx.is_fake == 1; } if (ctx.is_banned != null) { ctx.is_banned = ctx.is_banned == 1; }"
      }
    }
  ]
}'

for YEAR in {2018..2024}; do
  for MONTH in 01 02 03 04 05 06 07 08 09 10 11 12; do
    INDEX_NAME="tor-$YEAR-$MONTH"
    echo ""
    echo $INDEX_NAME
    echo ""

    sleep 3

    JSON_PAYLOAD=$(cat <<EOF
{
  "source": {
    "size": 50,
    "remote": {
      "host": "http://localhost:19200"
    },
    "index": "${INDEX_NAME}",
    "query": {
      "match_all": {}
    }
  },
  "dest": {
    "index": "${INDEX_NAME}",
    "pipeline": "convert_boolean"
  },
  "script": {
    "source": "if (ctx._source.containsKey('raw_text')) {ctx._source.remove('raw_text');} if (ctx._source.containsKey('raw_title')) {ctx._source.remove('raw_title');} if (ctx._source.containsKey('raw_url')) {ctx._source.remove('raw_url');}",
    "lang": "painless"
  }
}
EOF
)

    curl --cacert ${ES_CA_CERTS} --user ${ES_USERNAME}:${ES_PASSWORD} \
    -XPOST "${ES_URL}_reindex?pretty" \
    -H 'Content-Type: application/json' -d "$JSON_PAYLOAD"

    echo ""
  done
done
