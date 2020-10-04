class RPCError(Exception):
    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message


class ImproperlyConfigured(Exception):
    pass
