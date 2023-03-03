FROM python:3.9-slim-buster

WORKDIR /app

COPY dist/chatgpt-server-python /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

EXPOSE 50051

CMD ["./chatgpt-server-python"]
