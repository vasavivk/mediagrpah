FROM ubuntu:latest
COPY . .
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get -y install wget ffmpeg
RUN wget https://mediaarea.net/repo/deb/repo-mediaarea_1.0-21_all.deb
RUN dpkg -i repo-mediaarea_1.0-21_all.deb
RUN apt-get -y install mediainfo python3-pip sox
RUN pip install --upgrade pyrogram==1.4.16 tgcrypto telegraph python-dotenv m3u8 httpx
RUN chmod +x start.sh
