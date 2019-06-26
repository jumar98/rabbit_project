import pika
import sys
from utils.util_module import MessageTypeError, MESSAGE_TYPE, Logger
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

result_queue = channel.queue_declare(queue='', exclusive=True)

queue_name = result_queue.method.queue
channel.queue_bind(exchange='logs', queue=queue_name)


def callback(ch, method, properties, body):
    body_dict = eval(body.decode())
    receive_type = "".join(sys.argv[1:]).lower()
    Logger.filter_message(receive_type, body_dict)


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

try:
    receive_type = "".join(sys.argv[1:]).lower()
    if receive_type not in MESSAGE_TYPE:
        raise MessageTypeError

except MessageTypeError:
    print(f"This type <{receive_type}> is invalid")
    exit()
print(f"Waiting for a <{receive_type}> message...")
channel.start_consuming()