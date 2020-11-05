#!/usr/bin/env sh

docker run -d \
  --name elasticsearch-local \
  -p 9200:9200 \
  -p 9300:9300 \
  -v "$(pwd)/data:/usr/share/elasticsearch/data" \
  -v "$(pwd)/config:/usr/share/elasticsearch/config" \
  -e "discovery.type=single-node" \
  -e "http.cors.enabled=true" \
  -e "http.cors.allow-origin=*" \
  docker.elastic.co/elasticsearch/elasticsearch:7.0.0