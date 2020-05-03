# bitcoin-python-async-rpc
Lightweight Bitcoin async JSON-RPC Python client.

Serves as a tiny layer between an application and a Bitcoin daemon, its primary usage
is querying the current state of Bitcoin blockchain, network stats, transactions...

If you want complete Bitcoin experience in Python, consult
[python-bitcoinlib](https://github.com/petertodd/python-bitcoinlib) .

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
| `getblockhash` | ✔ |
| `getblockheader` | ✔ |
| `getblockstats` | ✔ |
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
Minimal illustration (assuming Python 3.8, where you can run `async` code in console)

```bash
$ python -m asyncio
>>> import asyncio
>>>
>>> from bitcoinrpc import BitcoinRPC
>>> rpc = BitcoinRPC("127.0.0.1", 8332, "rpc_user", "rpc_passwd")
>>> await rpc.getconnectioncount()
10
```