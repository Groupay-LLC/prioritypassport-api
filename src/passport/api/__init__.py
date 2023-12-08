from .customer import PassportCustomerAPI

__all__ = ["PassportAPI"]


class PassportAPI:
    def __init__(self, api_key: str, sandbox: bool = True):
        self.customer = PassportCustomerAPI(api_key, sandbox)
