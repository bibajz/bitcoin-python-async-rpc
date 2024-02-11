"""
Module containing definitions of objects (described as Python's Typed dictionaries)
taken from JSON-RPC 2.0 specification.

https://www.jsonrpc.org/specification
"""

from typing import List, Optional, Union

from typing_extensions import NotRequired, TypedDict

from bitcoinrpc._types import JSONType

RequestId = Union[int, str, None]
"""
https://www.jsonrpc.org/specification#request_object

According to the specification, must be String, Integer or Null.
"""


class Request(TypedDict):
    """
    https://www.jsonrpc.org/specification#request_object

    `jsonrpc` member is always "2.0"
    """

    jsonrpc: str
    id: RequestId
    method: str
    params: List[JSONType]


class Error(TypedDict):
    """
    https://www.jsonrpc.org/specification#error_object

    `data` member may not be present at all.
    """

    code: int
    message: str
    data: NotRequired[JSONType]


class _ResponseCommon(TypedDict):
    jsonrpc: str
    id: RequestId


class ResponseSuccess(_ResponseCommon):
    """
    https://www.jsonrpc.org/specification#response_object

    - `jsonrpc` member is always "2.0"
    - `result` member is always present and is a valid JSON
    - `error` should not be present by the specification, but at least Bitcoin Node
        as of version v26.0 always includes `error` member with value `NULL` on the
        success path.
    """

    result: JSONType
    error: NotRequired[Optional[Error]]


class ResponseError(_ResponseCommon):
    """
    https://www.jsonrpc.org/specification#response_object

    - `jsonrpc` member is always "2.0"
    - `result` should not be present by the specification, but at least Bitcoin Node
        as of version v26.0 always includes `result` member with value `NULL` on the
        error path.
    - `error` member is always present and is a JSON of `Error` shape defined above.
    """

    result: NotRequired[Optional[JSONType]]
    error: Error


Response = Union[ResponseSuccess, ResponseError]
