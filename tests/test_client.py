import typing as t

import httpx
import orjson
import pytest

from bitcoinrpc import BitcoinRPC


@pytest.mark.asyncio
async def test_two_clients_dont_share_counter(rpc_config: t.Dict[str, t.Any]) -> None:
    logs: t.List[bytes] = []

    def handler(_: httpx.Request) -> httpx.Response:
        """
        Mock the JSON-RPC response so this test does not rely on a running Bitcoin Node
        """
        return httpx.Response(200, json={"jsonrpc": "2.0", "id": 1, "result": 0})

    async def log_request(request: httpx.Request) -> None:
        """
        Hook that stores the serialized request before it is sent over the wire.
        """
        nonlocal logs
        logs.append(orjson.loads(request.content))

    url, auth = rpc_config["url"], rpc_config["auth"]
    client1 = httpx.AsyncClient(
        auth=auth,
        event_hooks={"request": [log_request]},
        transport=httpx.MockTransport(handler=handler),
    )
    client2 = httpx.AsyncClient(
        auth=auth,
        event_hooks={"request": [log_request]},
        transport=httpx.MockTransport(handler=handler),
    )

    async with BitcoinRPC(url=url, client=client1) as rpc1:
        _ = await rpc1.getblockcount()

    async with BitcoinRPC(url=url, client=client2) as rpc2:
        _ = await rpc2.getblockcount()

    req1, req2 = logs
    assert req1 == req2
