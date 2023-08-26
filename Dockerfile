FROM ubuntu:latest
COPY . .
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get -y install wget ffmpeg
RUN wget https://mediaarea.net/download/binary/mediainfo/23.07/mediainfo_23.07-1_amd64.xUbuntu_20.04.deb
RUN dpkg -i mediainfo_23.07-1_amd64.xUbuntu_20.04.deb && rm mediainfo_23.07-1_amd64.xUbuntu_20.04.deb
RUN apt-get update -y
RUN apt-get -y install mediainfo libmediainfo0 python3-pip sox
RUN pip install --upgrade bs4 lxml pyrogram tgcrypto pycryptodomex python-dotenv m3u8 httpx
RUN chmod +x start.sh
