import re

# Regular expression patterns for Bitcoin addresses
P2PKH_PATTERN = re.compile(r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$')
P2SH_PATTERN = re.compile(r'^3[a-km-zA-HJ-NP-Z1-9]{25,34}$')
BECH32_PATTERN = re.compile(r'^(bc1)[a-zA-HJ-NP-Z0-9]{25,39}$')

def is_valid_bitcoin_address(address: str) -> bool:
    return bool(P2PKH_PATTERN.fullmatch(address) or P2SH_PATTERN.fullmatch(address) or BECH32_PATTERN.fullmatch(address))

# Regular expression pattern for Bitcoin transaction hash
TX_HASH_PATTERN = re.compile(r'^[a-fA-F0-9]{64}$')

def is_valid_transaction_hash(tx_hash: str) -> bool:
    return bool(TX_HASH_PATTERN.fullmatch(tx_hash))