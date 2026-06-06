import pika
import json
from config import settings

class QueuePublisher:
    def __init__(self):
        self.host = settings.RABBITMQ_HOST
        self.queue = settings.RABBITMQ_QUEUE

    def publish_task(self, payload: dict) -> None:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue)
        
        channel.basic_publish(
            exchange='',
            routing_key=self.queue,
            body=json.dumps(payload)
        )
        connection.close()