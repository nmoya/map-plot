class HTTPError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


class NotFound(HTTPError):
    def __init__(self, message: str):
        super().__init__(404, message)


class Unauthorized(HTTPError):
    def __init__(self, message: str):
        super().__init__(401, message)
