from dataclasses import dataclass, asdict, field
from typing import Optional, TypeVar

from structlog import getLogger

from .base import BaseClient


logger = getLogger()


__all__ = [
    "TransactionRequestData",
    "TransactionIssueVirtualCardRequestData",
    "TransactionBookTransferRequestData",
    "DestinationEmailData",
    "DestinationAccountData",
    "DestinationData",
    "AccountData",
    "SourceAccountData",
    "CardIdData",
    "SourceCardData",
    "MerchantData",
    "ProcessingVirtualCardDetailData",
    "ProcessingBookTransferDetailData",
    "ProcessingCardPaymentDetailData",
    "SourceData",
    "CardProgramData",
    "VirtualCardData",
    "ProcessingDetailData",
    "PassportTransactionAPI",
]


@dataclass
class AccountData:
    """
    Priority Passport Account.
    """

    id: str


@dataclass
class DestinationEmailData:
    """
    Priority Passport Destination Email.
    """

    email: str


@dataclass
class DestinationAccountData:
    account: Optional[AccountData]


DestinationData = TypeVar("DestinationData", DestinationEmailData, DestinationAccountData)


@dataclass
class SourceAccountData:
    """
    Priority Passport Source.
    """

    account: AccountData


@dataclass
class CardIdData:
    """
    Priority Passport Card ID.
    """

    id: str


@dataclass
class SourceCardData:
    """
    Priority Passport Source.
    """

    card: CardIdData


SourceData = TypeVar("SourceData", SourceAccountData, SourceCardData)


@dataclass
class CardProgramData:
    """
    Priority Passport Card Program.
    """

    id: str


@dataclass
class VirtualCardData:
    """
    Priority Passport Virtual Card.
    """

    cardProgram: CardProgramData


@dataclass
class ProcessingVirtualCardDetailData:
    """
    Priority Passport Processing Virtual Card Detail.
    """

    virtualCard: VirtualCardData


@dataclass
class ProcessingBookTransferDetailData:
    """
    Priority Passport Processing Book Transfer.
    """

    memo: str = field(default="Transfer")


@dataclass
class MerchantData:
    """
    Priority Passport Merchant.
    """

    id: str


@dataclass
class ProcessingCardPaymentDetailData:
    """
    Priority Passport Processing Card Payment.
    """

    merchant: MerchantData
    statementDescriptor: str


ProcessingDetailData = TypeVar(
    "ProcessingDetailData",
    ProcessingVirtualCardDetailData,
    ProcessingBookTransferDetailData,
    ProcessingCardPaymentDetailData,
)


@dataclass
class TransactionRequestData:
    """
    Priority Passport Transaction Request.
    """

    externalId: str
    amount: str
    destination: DestinationData
    purpose: str
    source: SourceData
    processingDetail: ProcessingDetailData
    type: str
    method: str


@dataclass
class TransactionIssueVirtualCardRequestData(TransactionRequestData):
    """
    Priority Passport Issue Virtual Card Request.
    """

    destination: DestinationEmailData
    processingDetail: ProcessingVirtualCardDetailData
    type: str = field(default="REGULAR")
    method: str = field(default="VIRTUAL_CARD")
    allowDuplicate: str = field(default="true")


@dataclass
class TransactionBookTransferRequestData(TransactionRequestData):
    """
    Priority Passport Book Transfer Request.
    """

    processingDetail: ProcessingBookTransferDetailData
    destination: DestinationAccountData
    allowDuplicate: str = field(default="false")
    type: str = field(default="REGULAR")
    method: str = field(default="BOOK")


@dataclass
class TransactionCardPaymentRequestData(TransactionRequestData):
    processingDetail: ProcessingCardPaymentDetailData
    destination: DestinationAccountData
    type: str = field(default="REGULAR")
    method: str = field(default="CARD")


class PassportTransactionAPI(BaseClient):
    """
    Priority Passport Transaction API.
    """

    def issue_virtual_card(self, virtual_card_request: TransactionIssueVirtualCardRequestData) -> bool:
        post_req = self._post("/v1/transaction", data=asdict(virtual_card_request))
        if post_req.status_code == 201:
            logger.info(
                "Virtual Card Created", virtual_card_request_data=asdict(virtual_card_request), res=post_req.json()
            )
            return True
        else:
            logger.warning(
                "Unable to create Virtual Card",
                virtual_card_request_data=asdict(virtual_card_request),
                res=post_req.json(),
            )
            return False

    def book_transfer(self, book_transfer_request: TransactionBookTransferRequestData) -> bool:
        post_req = self._post("/v1/transaction", data=asdict(book_transfer_request))
        if post_req.status_code == 201:
            logger.info(
                "Book Transfer created", book_transfer_request=asdict(book_transfer_request), res=post_req.json()
            )
            return True
        else:
            logger.warning(
                "Unable to create Book Transfer",
                book_transfer_request=asdict(book_transfer_request),
                res=post_req.json(),
            )
            return False

    def card_payment(self, card_payment_request: TransactionCardPaymentRequestData) -> bool:
        post_req = self._post("/v1/transaction", data=asdict(card_payment_request))
        if post_req.status_code == 201:
            logger.info("Card Payment created", card_payment_request=asdict(card_payment_request), res=post_req.json())
            return True
        else:
            logger.warning(
                "Unable to create Card Payment",
                card_payment_request=asdict(card_payment_request),
                res=post_req.json(),
            )
            return False
