import pika
import time
import random
import base64
from io import BytesIO
from PIL import Image, ImageDraw

def generate_fake_image(label):
    img = Image.new('RGB', (64, 64), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    if label == 'face':
        draw.ellipse((20, 20, 44, 44), fill='blue')
    else:
        draw.rectangle((20, 20, 44, 44), fill='red')
    buf = BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode()

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials('guest', 'guest'))
)
channel = connection.channel()
channel.exchange_declare(exchange='imagens', exchange_type='topic')

while True:
    tipo = random.choice(['face', 'team'])
    img = generate_fake_image(tipo)
    channel.basic_publish(
        exchange='imagens',
        routing_key=tipo,
        body=img.encode()
    )
    print(f"[>] Enviada imagem tipo {tipo}")
    time.sleep(0.2)
