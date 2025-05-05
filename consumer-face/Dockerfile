FROM python:3.10-slim
WORKDIR /app
COPY consumer_face.py model_face.py .
RUN pip install pika pillow numpy
CMD ["python", "consumer_face.py"]
