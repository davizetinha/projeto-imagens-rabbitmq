FROM python:3.10-slim
WORKDIR /app
COPY consumer_team.py model_team.py .
RUN pip install pika pillow numpy
CMD ["python", "consumer_team.py"]
