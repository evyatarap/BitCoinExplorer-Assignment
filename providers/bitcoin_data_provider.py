from abc import ABC, abstractmethod
from typing import Optional
from pydantic import BaseModel
from typing import List

class AddressInfo(BaseModel):
    address: str
    balance: float
    transaction_count: int

class TransactionInput(BaseModel):
    address: str
    value: float

class TransactionOutput(BaseModel):
    address: str
    value: float

class TransactionInfo(BaseModel):
    hash: str
    fee: float  
    inputs: List[TransactionInput]
    outputs: List[TransactionOutput]
    transaction_index: int
    block_time: str 

class BitcoinDataProvider(ABC):
    @abstractmethod
    def get_address_info(self, address: str) -> Optional[AddressInfo]:
        pass

    @abstractmethod
    def get_transaction_info(self, tansaction_id: str) -> Optional[TransactionInfo]:
        pass