FROM python:3.10-slim
WORKDIR /app
COPY generator.py .
RUN pip install pika pillow numpy
CMD ["python", "generator.py"]
