FROM python:3.11.3-slim-buster

WORKDIR /app

ADD . /app

RUN apt-get update && apt-get install -y \
    build-essential \ 
    gcc \ 
    g++

RUN pip install --no-cache-dir -r requirements.txt

# docker build -t langbase .
# docker run -it -v $(pwd):/app -p 8501:8501 langbase bash 
# docker在windows下需要手写绝对路径
# streamlit run ./src/main.py