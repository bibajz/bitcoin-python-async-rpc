from typing import Any, Dict

import httpx
import pytest

from bitcoinrpc import BitcoinRPC


@pytest.mark.asyncio
async def test_connection_to_unknown_host(
    rpc_config: Dict[str, Any],
    unused_tcp_port: int,
) -> None:
    new_config = rpc_config.copy()
    new_config["url"] = f"http://localhost:{unused_tcp_port}"
    btc_rpc = BitcoinRPC.from_config(**new_config)

    with pytest.raises(httpx.ConnectError):
        await btc_rpc.getblockcount()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_connection_with_incorrect_auth(rpc_config: Dict[str, Any]) -> None:
    new_config = rpc_config.copy()
    new_config["auth"] = ("a", "b")
    btc_rpc = BitcoinRPC.from_config(**new_config)

    with pytest.raises(httpx.HTTPStatusError) as e:
        await btc_rpc.getblockcount()

    # 401 - Unauthorized
    assert e.value.response.status_code == 401


@pytest.mark.integration
@pytest.mark.asyncio
async def test_connection_and_sample_rpc(rpc_config: Dict[str, Any]) -> None:
    btc_rpc = BitcoinRPC.from_config(**rpc_config)

    block_count = await btc_rpc.getblockcount()

    assert block_count >= 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_connection_and_incorrect_rpc(rpc_config: Dict[str, Any]) -> None:
    """
    Incorrect values of arguments will not raise the `bitcoinrpc.RPCError`, but server error 500.
    """
    btc_rpc = BitcoinRPC.from_config(**rpc_config)

    with pytest.raises(httpx.HTTPStatusError) as e:
        await btc_rpc.getblockheader("???")

    # 500 - Internal server error
    assert e.value.response.status_code == 500
