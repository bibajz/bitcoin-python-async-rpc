FROM docker.io/debian:11.7-slim

ARG BTC_VERSION=v24.1

RUN apt-get update && \
  apt-get install -y \
    build-essential \
    libtool \
    autotools-dev \
    automake \
    pkg-config \
    bsdmainutils \
    python3 \
    libevent-dev \
    libboost-dev \
    libsqlite3-dev \
    libminiupnpc-dev \
    libnatpmp-dev \
    libzmq3-dev \
    systemtap-sdt-dev \
    git && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /opt

RUN git clone --depth 1 --branch ${BTC_VERSION} https://github.com/bitcoin/bitcoin && \
  cd bitcoin && \
  ./autogen.sh && \
  ./configure \
    --enable-debug \
    --enable-usdt \
    --with-sqlite=yes \
    --without-bdb \
    --with-miniupnpc \
    --with-natpmp \
    --with-utils \
    --with-daemon \
    --with-gui=no && \
  make -j$(nproc) && \
  make install  && \
  cd .. && \
  rm -rf bitcoin

RUN useradd --user-group --create-home rpc

USER rpc

WORKDIR /home/rpc

# Default data directory when running the bitcoin daemon on regtest
RUN mkdir -p .bitcoin/regtest

ENTRYPOINT ["/usr/local/bin/bitcoind", "-regtest", "-server"]

