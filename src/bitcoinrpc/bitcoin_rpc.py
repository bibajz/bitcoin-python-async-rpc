from typing import Any, Dict, List, Optional, TypeVar, Union

import httpx

import orjson

from typing_extensions import Literal


JSONData = TypeVar("JSONData", str, int, float, Dict, List, None)


class RPCError(Exception):
    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message


class BitcoinRPC:
    """
    Visit https://bitcoin.org/en/developer-reference for list of all commands
    """

    def __init__(self, host: str, port: int, rpc_user: str, rpc_password: str) -> None:
        self._url = self._set_url(host, port)
        self._client = self._set_client(rpc_user, rpc_password)

    @staticmethod
    def _set_url(host: str, port: int) -> str:
        return f"http://{host}:{port}"

    @staticmethod
    def _set_client(rpc_user: str, rpc_password: str) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            auth=(rpc_user, rpc_password), headers={"content-type": "application/json"}
        )

    @property
    def url(self) -> str:
        return self._url

    @property
    def client(self) -> httpx.AsyncClient:
        return self._client

    async def acall(
        self,
        method: str,
        params: List[Union[str, int, List[str], None]],
        **kwargs: Any,
    ) -> JSONData:
        """
        Pass keyword arguments to directly modify the constructed request -
            see `httpx.Request`.
        """
        req = self.client.post(
            url=self.url,
            data=orjson.dumps(
                {"jsonrpc": "2.0", "id": "1", "method": method, "params": params}
            ),
            **kwargs,
        )
        resp = orjson.loads((await req).content)

        if resp["error"] is not None:
            raise RPCError(resp["error"]["code"], resp["error"]["message"])
        else:
            return resp["result"]

    async def getmempoolinfo(self) -> JSONData:
        return await self.acall("getmempoolinfo", [])

    async def getmininginfo(self) -> JSONData:
        return await self.acall("getmininginfo", [])

    async def getnetworkinfo(self) -> JSONData:
        return await self.acall("getnetworkinfo", [])

    async def getblockchaininfo(self) -> JSONData:
        return await self.acall("getblockchaininfo", [])

    async def getconnectioncount(self) -> int:
        return await self.acall("getconnectioncount", [])

    async def getchaintips(self) -> JSONData:
        return await self.acall("getchaintips", [])

    async def getdifficulty(self) -> float:
        return await self.acall("getdifficulty", [])

    async def getbestblockhash(self) -> str:
        return await self.acall("getbestblockhash", [])

    async def getblockhash(self, height: int) -> str:
        return await self.acall("getblockhash", [height,])

    async def getblockheader(self, block_hash: str, verbose: bool = True) -> JSONData:
        return await self.acall("getblockheader", [block_hash, verbose])

    async def getblockstats(
        self,
        hash_or_height: Union[int, str],
        *keys: str,
        timeout: Optional[float] = None,
    ) -> JSONData:
        """
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
        timeout: Optional[float] = None,
    ) -> JSONData:
        """
        `verbosity`: 0 for hex-encoded block data, 1 for block data with transactions
            list, 2 for block data with each transaction.
        """
        return await self.acall(
            "getblock", [block_hash, verbosity], timeout=httpx.Timeout(timeout)
        )

    async def getrawtransaction(
        self,
        txid: str,
        verbose: bool = True,
        block_hash: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> JSONData:
        """
        :param txid: If transaction is not in mempool, block_hash must also be provided.
        :param verbose: True for JSON, False for hex-encoded
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
        timeout: Optional[float] = None,
    ) -> float:
        """
        :param nblocks: -1 for estimated hash power since last difficulty change,
            otherwise as an average over last provided number of blocks
        :param height: If not provided, get estimated hash power for the latest block
        :param timeout: If doing a lot of processing, no timeout may come in handy
        """
        return await self.acall(
            "getnetworkhashps", [nblocks, height], timeout=httpx.Timeout(timeout)
        )
