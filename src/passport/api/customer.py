from dataclasses import dataclass, asdict, field

from structlog import getLogger

from .base import BaseClient


logger = getLogger()


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
    usage: dict = field(default_factory=lambda: {"isPayorAddress": True})


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

    individual: IndividualData
    externalId: str
    type: str = field(default="individual")


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
            logger.info("Customer created", customer_data=asdict(customer_data))
            return True
        else:
            logger.warning("Unable to create customer", customer_data=asdict(customer_data), res=post_req.json())
            return False

    def create_customer_checking_account_by_id(self, customer_id: str) -> bool:
        """
        Create a checking account for a customer.
        """
        data = {"purpose": "checking"}
        post_req = self._post(f"/v1/customer/id/{customer_id}/account", data=data)
        if post_req.status_code == 201:
            logger.info("Customer checking account created", customer_id=customer_id)
            return True
        else:
            logger.warning("Unable to create customer checking account", customer_id=customer_id, res=post_req.json())
            return False

    def create_customer_checking_account_by_ext_id(self, external_id: str) -> bool:
        data = {"purpose": "checking"}
        post_req = self._post(f"/v1/customer/externalId/{external_id}/account", data=data)
        if post_req.status_code == 201:
            logger.info("Customer checking account created for external id", external_id=external_id)
            return True
        else:
            logger.warning(
                "Unable to create customer checking account for external id",
                external_id=external_id,
                res=post_req.json(),
            )
            return False

    def get_by_external_id(self, external_id: str) -> dict:
        """
        Get a customer by external ID.
        """
        get_customer = self._get(f"/v1/customer/externalId/{external_id}")
        if get_customer.status_code == 200:
            logger.info("Customer found by external id", external_id=external_id)
            return get_customer.json()
        else:
            logger.warning("Unable to find customer by external id", external_id=external_id, res=get_customer.json())
            return {}
