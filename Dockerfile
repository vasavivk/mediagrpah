FROM ubuntu:21.04
COPY . .
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get -y install libmediainfo0
RUN apt-get update -y
RUN apt-get -y install mediainfo python3-pip sox
RUN pip install --upgrade pyrogram==1.4.16 tgcrypto pycryptodomex python-dotenv httpx
RUN chmod +x start.sh
