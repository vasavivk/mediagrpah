FROM ubuntu:latest
COPY . .
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get -y install wget ffmpeg

RUN wget -q -O /tmp/libzen0.deb https://mediaarea.net/download/binary/libzen0/0.4.41/libzen0v5_0.4.41-1_amd64.xUbuntu_20.04.deb \
  && dpkg -i /tmp/libzen0.deb \
  && rm /tmp/libzen0.deb

RUN wget -q -O /tmp/libtinyxml2-6a.deb http://kr.archive.ubuntu.com/ubuntu/pool/universe/t/tinyxml2/libtinyxml2-6a_7.0.0+dfsg-1build1_amd64.deb \
  && dpkg -i /tmp/libtinyxml2-6a.deb \
  && rm /tmp/libtinyxml2-6a.deb

RUN wget -q -O /tmp/libmediainfo0.deb https://mediaarea.net/download/binary/libmediainfo0/23.07/libmediainfo0v5_23.07-1_amd64.xUbuntu_20.04.deb \
  && dpkg -i /tmp/libmediainfo0.deb \
  && rm /tmp/libmediainfo0.deb

RUN wget -q -O /tmp/mediainfo.deb https://mediaarea.net/download/binary/mediainfo/23.07/mediainfo_23.07-1_amd64.xUbuntu_20.04.deb \
  && dpkg -i /tmp/mediainfo.deb \
  && rm /tmp/mediainfo.deb

RUN apt-get -y install mediainfo python3-pip sox libsox-fmt-mp3 
RUN pip install --upgrade pyrogram==1.4.16 tgcrypto telegraph python-dotenv m3u8 httpx
RUN chmod +x start.sh
