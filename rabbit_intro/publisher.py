import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue="test")
for i in range(1,11):
    print(f"[X] Sent [{i}]")
    channel.basic_publish(exchange='', routing_key='test', body=f'Message {i}')
connection.close()
