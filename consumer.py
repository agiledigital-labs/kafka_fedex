from confluent_kafka import Consumer, KafkaError
import os
import requests

print("Start consumer")
c = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'fedex',
    'auto.offset.reset': 'earliest'
})

c.subscribe(['fedex'])

#If there is no such folder, the script will create one automatically
folder_location = r'TextFiles'
if not os.path.exists(folder_location):os.mkdir(folder_location)

while True:
    print("Something is true ;)")
    msg = c.poll(1.0)

    if msg is None:
        print("No messages :( ")
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue
    
    print('Received message: {}'.format(msg.value().decode('utf-8')))
    link = '{}'.format(msg.value().decode('utf-8'))
    
    filename = os.path.join(folder_location,link.split('/')[-1])
    with open(filename, 'wb') as f:
        f.write(requests.get(link).content)

print("You sad false fuck")
c.close()