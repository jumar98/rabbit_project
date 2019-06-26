import pika
import sys
import json
from utils.util_module import MessageTypeError, MESSAGE_TYPE

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')


try:
    message = " ".join(sys.argv[2:])
    message_type = sys.argv[1].lower()
    if not message:
        raise IndexError()
    if message_type not in MESSAGE_TYPE:
        raise MessageTypeError()
    body = {
        'message': message,
        'type': message_type
    }
except IndexError:
    print("You have to pass two parameter [type] - [message]")
    exit()
except MessageTypeError:
    print(f"The message type <{message_type}> is invalid")
    exit()

channel.basic_publish(exchange='logs', routing_key='',body=json.dumps(body))

print('[X] Sent')

connection.close()