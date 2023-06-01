import configparser
from pathlib import Path
from typing import Tuple

import pytest
from typing_extensions import TypedDict


class _RpcConfig(TypedDict):
    url: str
    auth: Tuple[str, str]


@pytest.fixture(scope="session")
def rpc_config() -> _RpcConfig:
    """
    Fixture of connection parameters usable by `BitcoinRPC.from_config`, kept in sync with bitcoin-regtest.conf
    file.
    """

    # Multiple `rpcallowip` keys within the config file, therefore parsing cannot be strict.
    parser = configparser.ConfigParser(strict=False)
    with open(Path(__file__).parent / "bitcoin-regtest.conf", encoding="utf-8") as f:
        parser.read_file(f)

    conf = parser["regtest"]
    _, port = conf["rpcbind"].split(":")
    return {
        "url": f"http://localhost:{port}",
        "auth": (conf["rpcuser"], conf["rpcpassword"]),
    }
