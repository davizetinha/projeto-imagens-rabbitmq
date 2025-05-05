import pika, base64, time
from io import BytesIO
from model_team import identificar_time

def callback(ch, method, properties, body):
    imagem = BytesIO(base64.b64decode(body))
    time.sleep(1)  # Simula IA lenta
    resultado = identificar_time(imagem)
    print(f"[TIME] Time identificado: {resultado}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Conexão com o RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials('guest', 'guest'))
)
channel = connection.channel()

# Declara a exchange do tipo topic
channel.exchange_declare(exchange='imagens', exchange_type='topic')

# Cria uma fila temporária exclusiva
queue = channel.queue_declare('', exclusive=True)
queue_name = queue.method.queue

# Faz binding da fila com routing_key 'team'
channel.queue_bind(exchange='imagens', queue=queue_name, routing_key='team')

print("[*] Aguardando brasões de times...")
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
channel.start_consuming()
