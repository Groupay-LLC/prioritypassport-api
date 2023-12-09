from .customer import PassportCustomerAPI

__all__ = ["PassportAPI"]


class PassportAPI:
    def __init__(self, api_key: str, sandbox: bool = True):
        self._api_key = api_key
        self._sanbox = sandbox
        self.customer = PassportCustomerAPI(api_key, sandbox)
