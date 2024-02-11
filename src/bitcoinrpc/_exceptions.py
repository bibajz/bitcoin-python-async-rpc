from bitcoinrpc._spec import Error, RequestId


class RPCError(Exception):
    """
    Enrich the `Error` - https://www.jsonrpc.org/specification#error_object
    with the `id` of the request that caused the error.
    """

    def __init__(self, id: RequestId, error: Error) -> None:
        super().__init__(error["message"])
        self.id = id
        self.error = error
