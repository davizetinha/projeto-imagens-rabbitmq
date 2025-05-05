import pika, base64, time
from io import BytesIO
from model_face import analisar_rosto

def callback(ch, method, properties, body):
    imagem = BytesIO(base64.b64decode(body))
    resultado = analisar_rosto(imagem)
    print(f"[FACE] Pessoa está: {resultado}")
    time.sleep(1)  # Simula processamento lento
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Confirma o processamento

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

# Faz binding da fila com routing_key 'face'
channel.queue_bind(exchange='imagens', queue=queue_name, routing_key='face')

print("[*] Aguardando imagens de rostos...")
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
channel.start_consuming()
