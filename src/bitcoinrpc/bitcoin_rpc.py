import itertools
from types import TracebackType
from typing import Any, Callable, List, Optional, Tuple, Type, Union

import httpx
import orjson
from typing_extensions import Literal, Self

from bitcoinrpc._exceptions import RPCError
from bitcoinrpc._types import (
    BestBlockHash,
    BitcoinRPCResponse,
    Block,
    BlockchainInfo,
    BlockCount,
    BlockHash,
    BlockHeader,
    BlockStats,
    ChainTips,
    ConnectionCount,
    Difficulty,
    MempoolInfo,
    MiningInfo,
    NetworkHashps,
    NetworkInfo,
    RawTransaction,
)

# Neat trick found in asyncio library for task enumeration
# https://github.com/python/cpython/blob/3.8/Lib/asyncio/tasks.py#L31
_next_rpc_id = itertools.count(1).__next__


class BitcoinRPC:
    __slots__ = ("_url", "_client", "_counter")
    """
    Class representing a JSON-RPC client of a Bitcoin node.

    :param url: URL of the Bitcoin node.
    :param client: Underlying `httpx.AsyncClient`, which handles the requests issued.
    :param counter: Optional callable that serves as a generator for the "id" field within JSON-RPC requests.

    For list of all available commands, visit:
    https://developer.bitcoin.org/reference/rpc/index.html
    """

    def __init__(
        self,
        url: str,
        client: httpx.AsyncClient,
        counter: Callable[[], Union[int, str]] = _next_rpc_id,
    ) -> None:
        self._url = url
        self._client = client
        self._counter = counter

    async def __aenter__(self) -> "BitcoinRPC":
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> None:
        await self.aclose()

    @classmethod
    def from_config(
        cls,
        url: str,
        auth: Optional[Tuple[str, str]],
        **options: Any,
    ) -> Self:
        """
        Instantiate the `BitcoinRPC` client while also configuring the underlying `httpx.AsyncClient`. Additional
        options are passed directly as kwargs to `httpx.AsyncClient`, so it's your responsibility to conform to its
        interface.
        """

        options = dict(options)
        headers = {
            "content-type": "application/json",
            **dict(options.pop("headers", {})),
        }
        return cls(url, httpx.AsyncClient(auth=auth, headers=headers, **options))

    @property
    def url(self) -> str:
        return self._url

    @property
    def client(self) -> httpx.AsyncClient:
        return self._client

    async def aclose(self) -> None:
        await self.client.aclose()

    async def acall(
        self,
        method: str,
        params: List[Union[str, int, List[str], None]],
        **kwargs: Any,
    ) -> BitcoinRPCResponse:
        """
        Pass keyword arguments to directly modify the constructed request -
            see `httpx.Request`.
        """
        response = await self.client.post(
            url=self.url,
            content=orjson.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": self._counter(),
                    "method": method,
                    "params": params,
                }
            ),
            **kwargs,
        )

        # Raise an exception if return code is not in 2xx range
        # https://www.python-httpx.org/quickstart/#exceptions
        response.raise_for_status()

        content = orjson.loads(response.content)
        if content["error"] is not None:
            raise RPCError(content["error"]["code"], content["error"]["message"])
        else:
            return content["result"]

    async def getmempoolinfo(self) -> MempoolInfo:
        """https://developer.bitcoin.org/reference/rpc/getmempoolinfo.html"""
        return await self.acall("getmempoolinfo", [])

    async def getmininginfo(self) -> MiningInfo:
        """https://developer.bitcoin.org/reference/rpc/getmininginfo.html"""
        return await self.acall("getmininginfo", [])

    async def getnetworkinfo(self) -> NetworkInfo:
        """https://developer.bitcoin.org/reference/rpc/getnetworkinfo.html"""
        return await self.acall("getnetworkinfo", [])

    async def getblockchaininfo(self) -> BlockchainInfo:
        """https://developer.bitcoin.org/reference/rpc/getblockchaininfo.html"""
        return await self.acall("getblockchaininfo", [])

    async def getconnectioncount(self) -> ConnectionCount:
        """https://developer.bitcoin.org/reference/rpc/getconnectioncount.html"""
        return await self.acall("getconnectioncount", [])

    async def getchaintips(self) -> ChainTips:
        """https://developer.bitcoin.org/reference/rpc/getchaintips.html"""
        return await self.acall("getchaintips", [])

    async def getdifficulty(self) -> Difficulty:
        """https://developer.bitcoin.org/reference/rpc/getdifficulty.html"""
        return await self.acall("getdifficulty", [])

    async def getbestblockhash(self) -> BestBlockHash:
        """https://developer.bitcoin.org/reference/rpc/getbestblockhash.html"""
        return await self.acall("getbestblockhash", [])

    async def getblockhash(self, height: int) -> BlockHash:
        """https://developer.bitcoin.org/reference/rpc/getblockhash.html"""
        return await self.acall("getblockhash", [height])

    async def getblockcount(self) -> BlockCount:
        """https://developer.bitcoin.org/reference/rpc/getblockcount.html"""
        return await self.acall("getblockcount", [])

    async def getblockheader(
        self, block_hash: str, verbose: bool = True
    ) -> BlockHeader:
        """https://developer.bitcoin.org/reference/rpc/getblockheader.html"""
        return await self.acall("getblockheader", [block_hash, verbose])

    async def getblockstats(
        self,
        hash_or_height: Union[int, str],
        *keys: str,
        timeout: Optional[float] = 5.0,
    ) -> BlockStats:
        """
        https://developer.bitcoin.org/reference/rpc/getblockstats.html

        Enter `keys` as positional arguments to return only the provided `keys`
            in the response.
        """
        return await self.acall(
            "getblockstats",
            [hash_or_height, list(keys) or None],
            timeout=httpx.Timeout(timeout),
        )

    async def getblock(
        self,
        block_hash: str,
        verbosity: Literal[0, 1, 2] = 1,
        timeout: Optional[float] = 5.0,
    ) -> Block:
        """
        https://developer.bitcoin.org/reference/rpc/getblock.html

        :param verbosity: 0 for hex-encoded block data, 1 for block data with
            transactions list, 2 for block data with each transaction.
        """
        return await self.acall(
            "getblock", [block_hash, verbosity], timeout=httpx.Timeout(timeout)
        )

    async def getrawtransaction(
        self,
        txid: str,
        verbose: bool = True,
        block_hash: Optional[str] = None,
        timeout: Optional[float] = 5.0,
    ) -> RawTransaction:
        """
        https://developer.bitcoin.org/reference/rpc/getrawtransactiono.html

        :param txid: If transaction is not in mempool, block_hash must also be provided.
        :param verbose: True for JSON, False for hex-encoded string
        :param block_hash: see ^txid
        :param timeout: If doing a lot of processing, no timeout may come in handy
        """
        return await self.acall(
            "getrawtransaction",
            [txid, verbose, block_hash],
            timeout=httpx.Timeout(timeout),
        )

    async def getnetworkhashps(
        self,
        nblocks: int = -1,
        height: Optional[int] = None,
        timeout: Optional[float] = 5.0,
    ) -> NetworkHashps:
        """
        https://developer.bitcoin.org/reference/rpc/getnetworkhashps.html

        :param nblocks: -1 for estimated hash power since last difficulty change,
            otherwise as an average over last provided number of blocks
        :param height: If not provided, get estimated hash power for the latest block
        :param timeout: If doing a lot of processing, no timeout may come in handy
        """
        return await self.acall(
            "getnetworkhashps", [nblocks, height], timeout=httpx.Timeout(timeout)
        )
