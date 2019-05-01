import json
import sys
from kafka import KafkaConsumer
from pymongo import MongoClient


client = MongoClient("localhost", 27017)
db = client.badcomments
collection = db[sys.argv[1]]

consumer = KafkaConsumer(
    sys.argv[1],
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id=str("my_group_" + sys.argv[1]),
    value_deserializer=lambda x: json.loads(x.decode('utf-8')))

for message in consumer:
    message = message.value
    collection.insert_one(message)

