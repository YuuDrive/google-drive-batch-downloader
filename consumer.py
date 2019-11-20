import pika
from lib.google import GDirect
from dotenv import load_dotenv
import json, os

load_dotenv()

RABBIT_CHANNEL = os.getenv('RABBIT_CHANNEL')
RABBIT_HOST = os.getenv('RABBIT_HOST')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBIT_HOST))
channel = connection.channel()

channel.queue_declare(queue=RABBIT_CHANNEL)

def callback(ch, method, properties, body):
    body = json.loads(body)
    print(" [x] Received %r" % body.get('id'))

    dl = GDirect()
    dl.get_direct(body.get('id'))
    dl.download()


channel.basic_consume(queue=RABBIT_CHANNEL, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()