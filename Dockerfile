FROM python:3.9-slim-buster as builder
WORKDIR /app
ADD chatgpt-server-python.tar.gz /app
WORKDIR /app
# pip换中国源
RUN pip install tiktoken
RUN mkdir -p ~/.pip || true
RUN echo "[global]" > ~/.pip/pip.conf
RUN echo "index-url = https://pypi.tuna.tsinghua.edu.cn/simple" >> ~/.pip/pip.conf
RUN echo "[install]" >> ~/.pip/pip.conf
RUN echo "trusted-host = pypi.tuna.tsinghua.edu.cn" >> ~/.pip/pip.conf
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
