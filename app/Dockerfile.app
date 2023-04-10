FROM python:3.9

LABEL maintainer "Jerry Kim"

RUN sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list
RUN sed -i 's/security.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
RUN apt-get install -y \
        build-essential \
        cmake \
        vim \
        git \
        curl \
        wget \
        ca-certificates \
        libjpeg-dev \
        libpng-dev \
        libgl1-mesa-glx \
        libglib2.0-0

RUN apt-get update && apt-get -y upgrade

COPY requirements.txt /tmp
WORKDIR "/tmp"
RUN pip3 install -r requirements.txt && \ 
        rm /tmp/*

WORKDIR "/app"
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8001"]
