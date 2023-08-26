FROM ubuntu:latest
COPY . .
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    python3-pip \
    libtinyxml2-9 \
    libcurl3-gnutls \
    libmms0 \
    libzen0v5 \
    libcurl4-gnutls-dev \
    libzen-dev \
    wget \
    ffmpeg \
    libsox-fmt-mp3 \
    sox

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

RUN wget -q -O /tmp/mediainfo.deb https://mediaarea.net/download/binary/mediainfo/22.12/mediainfo_22.12-1_amd64.xUbuntu_20.04.deb \
  && dpkg -i /tmp/mediainfo.deb \
  && rm /tmp/mediainfo.deb

RUN pip install --upgrade pyrogram==1.4.16 tgcrypto telegraph python-dotenv m3u8 httpx
RUN chmod +x start.sh
