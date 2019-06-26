import pika
import time
import random

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue="test")


def callback(ch, method, properties, body):
    seek = random.randint(1,10)
    time.sleep(seek)
    print(f"[X] received {body.decode()} and I sleep by {seek}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="test", on_message_callback=callback, )

print("Waiting for a message...")
channel.start_consuming()