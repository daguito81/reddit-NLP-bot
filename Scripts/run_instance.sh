#!/bin/bash


/opt/kafka/bin/kafka-topics.sh --create --replication-factor 1 --partitions 1 --bootstrap-server localhost:9092 --topic $1

python commentcatcher.py $1
