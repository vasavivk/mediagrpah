FROM ubuntu:latest

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 LANGUAGE=en_US:en TZ=Asia/Kolkata

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
    python3-pip \
    git \
    libtinyxml2-9 \
    libcurl3-gnutls \
    libmms0 \
    libzen0v5 \
    libcurl4-gnutls-dev \
    libzen-dev \
    wget \
    ffmpeg \
    libsox-fmt-mp3 \
    sox \
    locales \
    megatools \
  && rm -rf /var/lib/apt/lists/*

RUN wget -q -O /tmp/libzen0.deb https://mediaarea.net/download/binary/libzen0/0.4.41/libzen0v5_0.4.41-1_amd64.Ubuntu_22.10.deb \
  && dpkg -i /tmp/libzen0.deb \
  && rm /tmp/libzen0.deb

RUN wget -q -O /tmp/libmediainfo0.deb https://mediaarea.net/download/binary/libmediainfo0/23.10/libmediainfo0v5_23.10-1_amd64.xUbuntu_22.04.deb \
  && dpkg -i /tmp/libmediainfo0.deb \
  && rm /tmp/libmediainfo0.deb

RUN wget -q -O /tmp/mediainfo.deb https://mediaarea.net/download/binary/mediainfo/23.04/mediainfo_23.04-1_amd64.Ubuntu_22.10.deb \
  && dpkg -i /tmp/mediainfo.deb \
  && rm /tmp/mediainfo.deb

RUN locale-gen en_US.UTF-8 && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

RUN pip install --upgrade pyrogram tgcrypto telegraph python-dotenv m3u8 requests bs4
COPY . .
RUN chmod +x start.sh
CMD ["bash", "start.sh"]
