#!/bin/bash


# Usage: testredditpipe.sh sub1 sub2 sub3

echo "Kafka Topics"

for topic in "$@"
do
echo ----------------
/opt/kafka/bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic $topic --time -1
done
