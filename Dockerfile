FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

RUN apt-get update && apt-get install -y libglib2.0-0

RUN apt-get update \
    && apt-get install -y \
    build-essential \
    curl \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-dev \
    python3.8 \
    python3-pip \
    && ln -s /usr/bin/python3.8 /usr/local/bin/python

WORKDIR mvs

COPY . ./

RUN pip3 install -r requirements.txt

RUN mkdir /mvs/fusible/build
WORKDIR /mvs/fusible/build
RUN cmake ..
RUN make
WORKDIR /mvs
