FROM ubuntu:latest
COPY . .
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get -y install wget ffmpeg
RUN wget -q -O /tmp/libzen0v5.deb http://th.archive.ubuntu.com/ubuntu/pool/universe/libz/libzen/libzen0v5_0.4.40-1_amd64.deb \
  && dpkg -i /tmp/libzen0v5.deb \
  && rm /tmp/libzen0v5.deb

RUN wget -q -O /tmp/libmediainfo0v5.deb http://ftp.de.debian.org/debian/pool/main/libm/libmediainfo/libmediainfo0v5_22.12+dfsg-1_amd64.deb \
  && dpkg -i /tmp/libmediainfo0v5.deb \
  && rm /tmp/libmediainfo0v5.deb

RUN wget -q -O /tmp/libtinyxml2-6a.deb http://kr.archive.ubuntu.com/ubuntu/pool/universe/t/tinyxml2/libtinyxml2-6a_7.0.0+dfsg-1build1_amd64.deb \
  && dpkg -i /tmp/libtinyxml2-6a.deb \
  && rm /tmp/libtinyxml2-6a.deb

RUN wget -q -O /tmp/libmediainfo-dev.deb http://ftp.de.debian.org/debian/pool/main/libm/libmediainfo/libmediainfo-dev_22.12+dfsg-1_amd64.deb \
  && dpkg -i /tmp/libmediainfo-dev.deb \
  && rm /tmp/libmediainfo-dev.deb

RUN wget -q -O /tmp/mediainfo.deb https://mediaarea.net/download/binary/mediainfo/23.07/mediainfo_23.07-1_amd64.xUbuntu_20.04.deb \
  && dpkg -i /tmp/mediainfo.deb \
  && rm /tmp/mediainfo.deb
RUN apt-get update -y
RUN apt-get -y install mediainfo libmediainfo0 python3-pip sox
RUN pip install --upgrade bs4 lxml pyrogram tgcrypto pycryptodomex python-dotenv m3u8 httpx
RUN chmod +x start.sh
