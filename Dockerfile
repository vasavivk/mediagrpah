FROM ubuntu:latest

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 LANGUAGE=en_US:en TZ=Asia/Kolkata

WORKDIR /usr/src/app
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get -y install libmediainfo0
RUN apt-get update -y
RUN apt-get -y install mediainfo python3-pip sox
RUN pip install --upgrade pyrogram==1.4.16 tgcrypto pycryptodomex python-dotenv httpx
COPY . .
RUN chmod +x start.sh
