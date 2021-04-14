#!/usr/bin/env bash

docker run \
  --rm \
  --network host \
  --env RPCUSER="rpc_user" \
  --env RPCPASSWORD="rpc_password" \
  --mount type=volume,src=bitcoind-data,target=/bitcoin \
  --name=bitcoind-node \
  bitcoindevelopernetwork/bitcoind-regtest
