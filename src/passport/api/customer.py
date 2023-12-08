from dataclasses import dataclass, asdict

from .base import BaseClient


__all__ = [
    "MailingAddressData",
    "IndividualData",
    "PassportCustomerData",
    "PassportCustomerAPI",
]


@dataclass
class MailingAddressData:
    """
    Priority Passport Mailing Address.
    """

    addressLine1: str
    addressLine2: str
    city: str
    state: str
    zip: str
    isPrimary: bool
    usage: dict = {"isPayorAddress": True}


@dataclass
class IndividualData:
    """
    Priority Passport Individual.
    """

    firstName: str
    lastName: str
    email: str
    mailingAddress: list[MailingAddressData]


@dataclass
class PassportCustomerData:
    """
    Priority Passport Customer.
    """

    type: str = "INDIVIDUAL"
    individual: IndividualData
    externalId: str


class PassportCustomerAPI(BaseClient):
    """
    Priority Passport Customer API.
    """

    def create_customer(self, customer_data: PassportCustomerData) -> bool:
        """
        Create a customer.
        """
        post_req = self._post("/v1/customer", data=asdict(customer_data))
        if post_req.status_code == 201:
            return True
        else:
            return False

    def create_customer_checking_account(self, customer_id: str) -> bool:
        """
        Create a checking account for a customer.
        """
        data = {"purpose": "checking"}
        post_req = self._post(f"/v1/customer/id/{customer_id}/account")
        if post_req.status_code == 201:
            return True
        else:
            return False

    def get_by_external_id(self, external_id: str) -> dict:
        """
        Get a customer by external ID.
        """
        return self._get(f"/v1/customer/externalId/{external_id}").json()
