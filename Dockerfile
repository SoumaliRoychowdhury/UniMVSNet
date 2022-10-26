FROM nvidia/cudagl:11.1-devel-ubuntu20.04

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
    cmake \
    libopencv-dev \
    && ln -s /usr/bin/python3.8 /usr/local/bin/python

WORKDIR mvs

COPY . ./

RUN pip3 install -r requirements.txt
#
RUN mkdir /mvs/fusibile/build
WORKDIR /mvs/fusibile/build
#RUN cmake ..
#RUN make
#WORKDIR /mvs
