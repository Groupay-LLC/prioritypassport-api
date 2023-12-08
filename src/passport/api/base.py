"""
Priority Passport API (limited feature implementation).
"""
from requests import get, post

__all__ = [
    "BaseClient",
]


class BaseClient:
    def __init__(self, api_key: str, sandbox: bool = True):
        self._api_key = api_key
        self._sanbox = sandbox
        if self._sanbox:
            self.base_url = "https://api.sandbox.prioritypassport.com"
        else:
            self.base_url = "https://api.prioritypassport.com"
            raise ValueError("NOTE: Production API not yet supported!!")

    def _get(self, endpoint: str, params: dict = None):
        if params is None:
            params = {}
        params["api_key"] = self._api_key
        return get(self.base_url + endpoint, params=params)

    def _post(self, endpoint: str, data: dict = None, params: dict = None):
        if data is None:
            raise ValueError("POST data cannot be None")
        if params is None:
            params = {}
        params["api_key"] = self._api_key
        return post(self.base_url + endpoint, data=data, params=params)
