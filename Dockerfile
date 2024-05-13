FROM python:3-alpine

ENV BOT_TOKENT=''

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt
CMD ["python3", "bot/main.py"]