FROM ubuntu:latest
COPY . .
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get -y install wget ffmpeg libmediainfo0v5 libmediainfo-dev
RUN wget -q -O /tmp/libzen0v5.deb http://th.archive.ubuntu.com/ubuntu/pool/universe/libz/libzen/libzen0v5_0.4.40-1_amd64.deb \
  && dpkg -i /tmp/libzen0v5.deb \
  && rm /tmp/libzen0v5.deb

RUN wget -q -O /tmp/libtinyxml2-6a.deb http://kr.archive.ubuntu.com/ubuntu/pool/universe/t/tinyxml2/libtinyxml2-6a_7.0.0+dfsg-1build1_amd64.deb \
  && dpkg -i /tmp/libtinyxml2-6a.deb \
  && rm /tmp/libtinyxml2-6a.deb

RUN wget -q -O /tmp/mediainfoall.deb https://mediaarea.net/repo/deb/repo-mediaarea_1.0-21_all.deb \
  && dpkg -i /tmp/mediainfoall.deb \
  && rm /tmp/mediainfoall.deb
RUN apt-get update -y
RUN apt-get -y install mediainfo libmediainfo0 python3-pip sox
RUN pip install --upgrade bs4 lxml pyrogram tgcrypto pycryptodomex python-dotenv m3u8 httpx
RUN chmod +x start.sh
