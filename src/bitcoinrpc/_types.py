from typing import Any, Dict, List, TypeVar, Union

from typing_extensions import Literal, NotRequired, TypedDict

JSONType = Union[None, bool, int, float, str, List["JSONType"], Dict[str, "JSONType"]]

# Type aliases for 1-to-1 match of RPC method and its return type
ConnectionCount = int
Difficulty = float
BestBlockHash = str
BlockHash = str
BlockCount = int
NetworkHashps = float
CombinePSBT = str
JoinPSBTs = str
UtxoUpdatePSBT = str


class MempoolInfo(TypedDict):
    loaded: bool
    size: int
    bytes: int
    usage: int
    maxmempoool: int
    mempoolminfee: float
    mempoolmaxfee: float


class _NetworkInfoNetworks(TypedDict):
    name: str
    limited: bool
    reachable: bool
    proxy: str
    proxy_randomize_credentials: bool


class _NetworkInfoAddresses(TypedDict):
    address: str
    port: int
    score: float


class NetworkInfo(TypedDict):
    version: int
    subversion: str
    protocolversion: str
    localservices: str
    localservicenames: List[str]
    localrelay: bool
    timeoffset: int
    networkactive: bool
    networks: List["_NetworkInfoNetworks"]
    relayfee: float
    incrementalfee: float
    localaddresses: List["_NetworkInfoAddresses"]
    warnings: str


class BlockchainInfo(TypedDict):
    # TODO: Shares common items with MiningInfo
    chain: Literal["main", "test", "regtest"]
    blocks: int
    headers: int
    bestblockhash: str
    difficulty: float
    mediantime: int
    verificationprogress: float
    initialblockdownload: bool
    chainwork: str
    size_on_disk: int
    pruned: bool
    softforks: Dict[str, Any]  # dictionary of the format {"bip-xxx": {...}}
    warnings: str


class _ChainTipsDetail(TypedDict):
    height: int
    hash: str
    branchlen: int
    status: Literal["active", "valid-fork", "valid-headers", "headers-only", "invalid"]


ChainTips = List["_ChainTipsDetail"]


class _BlockHeader(TypedDict):
    """
    Returned when verbose is set to `True`. Otherwise, `str` is returned
    """

    hash: str
    confirmations: int
    height: int
    version: int
    versionHex: str
    merkleroot: str
    time: int
    mediantime: int
    nonce: int
    bits: str
    difficulty: float
    chainwork: str
    nTx: int
    previousblockhash: str
    nextblockhash: str


BlockHeader = Union[str, "_BlockHeader"]


class BlockStats(TypedDict):
    """
    Returned dictionary will contain subset of the following, depending on filtering.
    """

    avgfee: int
    avgfeerate: int
    avgtxsize: int
    blockhash: str
    feerate_percentiles: List[int]
    heigth: int
    ins: int
    maxfee: int
    maxfeerate: int
    maxtxsize: int
    medianfee: int
    mediantime: int
    mediantxsize: int
    minfee: int
    minfeerate: int
    mintxsize: int
    outs: int
    subsidy: int  # Block reward in Satoshis
    swtotal_size: int
    swtotal_weight: int
    swtxs: int
    time: int
    total_out: int
    total_size: int
    total_weight: int
    totalfee: int
    txs: int
    utxo_increase: int
    utxo_size_inc: int


class Block(_BlockHeader):
    strippedsize: int
    tx: List["RawTransaction"]


class _RawTransaction(TypedDict):
    """Returned when verbose is set to `True`. Otherwise, `str` is returned"""

    txid: str
    hash: str
    version: int
    size: int
    vsize: int
    weight: int
    locktime: int
    vin: List[Dict[str, Any]]  # TODO: Complete
    vout: List[Dict[str, Any]]  # TODO: Complete
    hex: str
    blockhash: str
    confirmations: str
    time: int
    blocktime: int


RawTransaction = Union[str, "_RawTransaction"]


class MiningInfo(TypedDict):
    # TODO: Shares common items with BlockchainInfo
    blocks: int
    difficulty: float
    networkhashps: float
    pooledtx: int
    chain: Literal["main", "test", "regtest"]
    warnings: str


class AnalyzePSBT(TypedDict):
    inputs: List[Dict[str, Any]]  # TODO: Complete
    next: str

    fee: NotRequired[float]
    estimated_vsize: NotRequired[float]
    estimated_feerate: NotRequired[float]
    error: NotRequired[str]


class DecodePSBT(TypedDict):
    tx: Dict[str, Any]
    unknown: Dict[str, Any]
    inputs: List[Dict[str, Any]]
    outputs: List[Dict[str, Any]]

    fee: NotRequired[float]


class FinalizePSBT(TypedDict):
    psbt: str
    hex: str
    complete: bool


class WalletProcessPSBT(TypedDict):
    psbt: str
    complete: bool


BitcoinRPCResponse = TypeVar(
    "BitcoinRPCResponse",
    ConnectionCount,
    Difficulty,
    BestBlockHash,
    BlockHash,
    BlockCount,
    NetworkHashps,
    MempoolInfo,
    MiningInfo,
    BlockchainInfo,
    NetworkInfo,
    ChainTips,
    BlockHeader,
    BlockStats,
    Block,
    RawTransaction,
    CombinePSBT,
    JoinPSBTs,
    UtxoUpdatePSBT,
    AnalyzePSBT,
    DecodePSBT,
    FinalizePSBT,
    WalletProcessPSBT,
)
