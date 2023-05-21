# bitcoin-python-async-rpc
Lightweight Bitcoin async JSON-RPC Python client.

Serves as a tiny layer between an application and a Bitcoin daemon, its primary usage
is querying the current state of Bitcoin blockchain, network stats, transactions...

If you want complete Bitcoin experience in Python, consult
[python-bitcoinlib](https://github.com/petertodd/python-bitcoinlib).

## Installation
```bash
$ pip install bitcoinrpc
```

## Supported methods
Here is a list of supported methods, divided by their categories. Should you need
method not implemented, wrap the call in `BitcoinRPC.acall(<your_method>, ...)` coroutine.

### Blockchain

|   Method   |   Supported?     |
|------------|:----------------:|
| `getbestblockhash` | ✔ |
| `getblock` | ✔ |
| `getblockchaininfo` | ✔ |
| `getblockcount` | ✔ |
| `getblockhash` | ✔ |
| `getblockheader` | ✔ |
| `getblockstats` | ✔ |
| `getchaintips` | ✔ |
| `getdifficulty` | ✔ |
| `getmempoolinfo` | ✔ |
| `getnetworkhashps` | ✔ |

### Mining

|   Method   |   Supported?     |
|------------|:----------------:|
| `getmininginfo` | ✔ |

### Network

|   Method   |   Supported?     |
|------------|:----------------:|
| `getconnectioncount` | ✔ |
| `getnetworkinfo` | ✔ |

### Raw transactions

|   Method   |   Supported?     |
|------------|:----------------:|
| `getrawtransaction` | ✔ |

## Usage
Minimal illustration (assuming Python 3.8+, where you can run `async` code in console)

```
$ python -m asyncio
>>> import asyncio
>>>
>>> from bitcoinrpc import BitcoinRPC
>>> rpc = BitcoinRPC("http://localhost:18443" "rpc_user", "rpc_passwd")
>>> await rpc.getconnectioncount()
10
>>> await rpc.aclose()  # Clean-up resource
```

You can also use the `BitcoinRPC` as an asynchronous context manager, which does
all the resource clean-up automatically, as the following example shows:

```
$ cat btc_rpc_minimal.py
import asyncio

from bitcoinrpc import BitcoinRPC


async def main():
    async with BitcoinRPC("http://localhost:18443", "rpc_user", "rpc_password") as rpc:
        print(await rpc.getconnectioncount())


if __name__ == "__main__":
    asyncio.run(main())
```

Running this script yields:
```
$ python btc_rpc_minimal.py
10
```

## Testing

A `Containerfile` is provided as a means to build an OCI image of a Bitcoin `regtest` node.
Build the image (`podman` is used, but `docker` should be fine too):

```
$ podman build \
  -f Containerfile \
  --build-arg BTC_VERSION=v24.1 \
  -t bitcoin-regtest:v24.1 \
  -t bitcoin-regtest:latest \
  .
```

and run it afterwards:

```
$ podman run \
  --rm \
  -it \
  --mount=type=bind,src=./tests/bitcoin-regtest.conf,target=/home/rpc/.bitcoin/bitcoin.conf \
  -p 127.0.0.1:18443:18443 \
  --name bitcoin-regtest \
  localhost/bitcoin-regtest:v24.1
```

which will expose the Bitcoin `regtest` node on port 18443, accesible from localhost only, with RPC user/password `rpc_user/rpc_password`.

After you are done testing, stop the container via:

```
$ podman stop bitcoin-regtest
```

---

If you want to test against a different version of Bitcoin node, pass a different [tag](https://github.com/bitcoin/bitcoin/tags) in the build stage:

```
$ podman build \
  -f Containerfile \
  --build-arg BTC_VERSION=v25.0 \
  -t bitcoin-regtest:v25.0 \
  -t bitcoin-regtest:latest \
  .
```

---

Different settings of the Bitcoin node may be passed via mounting your custom configuration file, or optionally as "arguments" to `podman run`:


```
$ podman run \
  --rm \
  -it \
  --mount=type=bind,src=<path/to/your/config_file>,target=/home/rpc/.bitcoin/bitcoin.conf \
  -p 127.0.0.1:18443:18443 \
  --name bitcoin-regtest \
  localhost/bitcoin-regtest:v24.1 <your> <args> ...
```

---

Please, keep in mind that Bitcoin node compiled in the image is intended for testing & debugging purposes only! It may serve you as an inspiration for building
your own, production-ready Bitcoin node, but its intended usage is testing!

## Changelog

- **2021/12/28 - 0.5.0** change the signature of `BitcoinRPC` from `host, port, ...` to `url, ...`, delegating the creation of the node url to the caller.

## License
MIT
