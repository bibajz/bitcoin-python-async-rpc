import itertools
from types import TracebackType
from typing import Any, List, Optional, Type, Union

import httpx
import orjson
from typing_extensions import Literal

from ._exceptions import ImproperlyConfigured, RPCError
from ._types import (
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
    __slots__ = ("_url", "_client")
    """
    For list of all available commands, visit:
    https://developer.bitcoin.org/reference/rpc/index.html
    """

    def __init__(
        self, host: str, port: int, rpc_user: str, rpc_password: str, **options: Any
    ) -> None:
        self._url = self._set_url(host, port)
        self._client = self._configure_client(rpc_user, rpc_password, **options)

    async def __aenter__(self) -> "BitcoinRPC":
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> None:
        await self.aclose()

    @staticmethod
    def _set_url(host: str, port: int) -> str:
        return f"http://{host}:{port}"

    @staticmethod
    def _configure_client(
        rpc_user: str, rpc_password: str, **options: Any
    ) -> httpx.AsyncClient:
        """
        Configure `httpx.AsyncClient`. If you choose to provide additional options, it
        is your responsibility to conform to the `httpx.AsyncClient` interface.
        """
        auth = (rpc_user, rpc_password)
        headers = {"content-type": "application/json"}

        options = dict(options)
        if not options:
            return httpx.AsyncClient(auth=auth, headers=headers)

        if "auth" in options:
            raise ImproperlyConfigured("Authentication cannot be set via options!")

        if "headers" in options:
            _additional_headers = dict(options.pop("headers"))
            headers.update(_additional_headers)
            # guard against content-type overwrite
            headers["content-type"] = "application/json"

        return httpx.AsyncClient(auth=auth, headers=headers, **options)

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
        req = self.client.post(
            url=self.url,
            data=orjson.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": _next_rpc_id(),
                    "method": method,
                    "params": params,
                }
            ),
            **kwargs,
        )
        resp = orjson.loads((await req).content)

        if resp["error"] is not None:
            raise RPCError(resp["error"]["code"], resp["error"]["message"])
        else:
            return resp["result"]

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
