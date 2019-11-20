import pika
import json
from dotenv import load_dotenv
import os

load_dotenv()

RABBIT_CHANNEL = os.getenv('RABBIT_CHANNEL')
RABBIT_HOST = os.getenv('RABBIT_HOST')

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
channel = connection.channel()

channel.queue_declare(queue=RABBIT_CHANNEL)

ids_list = """
1kwVy4xUiPUGmGM3GKzP1SiWnv52dcqXS
1fh8-q0SjnllflBmzaWjkqg04OmiinRKw
"""

ids_list = ids_list.splitlines()
ids_list = list(filter(None, ids_list))

for i in ids_list:
    body = {
        "id": i,
    }
    channel.basic_publish(exchange='', routing_key=RABBIT_CHANNEL, body=json.dumps(body))
    print(" [x] Sent {}".format(json.dumps(body)))

connection.close()