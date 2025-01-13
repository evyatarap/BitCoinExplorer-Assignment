from providers.bitcoin_data_provider import BitcoinDataProvider
import requests
import logging


class BlockCypherProvider(BitcoinDataProvider):
    
    def __init__(self):
        self.base_url = "https://api.blockcypher.com/v1/btc/main"
        self.address_url = f"{self.base_url}/addrs"
        self.transaction_url = f"{self.base_url}/txs"
        self.block_url = f"{self.base_url}/blocks"
        self.headers = {
            "Content-Type": "application/json"
        }
        self.logger = logging.getLogger(__name__)
        
    def get_address_info(self, bitcoin_address: str):
        response = requests.get(f"{self.address_url}/{bitcoin_address}", headers=self.headers)
        if response.status_code == 200:
            data = response.json()

            if "address" not in data or \
                "balance" not in data or \
                "n_tx" not in data:
                self.logger.error(f"Invalid response data: {data}")
                return None

            address_info = {
                "address": data["address"],
                "balance": data["balance"] / 1e8,  # Convert satoshis to BTC,
                "transaction_count": data["n_tx"]
            }
            return address_info
        else:
            return None

    def get_transaction_info(self, transaction_id: str):
        response = requests.get(f"{self.transaction_url}/{transaction_id}", headers=self.headers)
        if response.status_code == 200:
            data = response.json()

            #TODO: Validate the response data

            inputs = []
            for item in data["inputs"]:
                inputs.append({
                    "address": item["addresses"][0],
                    "value": item["output_value"] / 1e8
                })
            
            outputs = []
            for item in data["outputs"]:
                outputs.append({
                    "address": item["addresses"][0],
                    "value": item["value"] / 1e8
                })

            transaction_info = {
                "hash": data["hash"],
                "fee": data["fees"] / 1e8,
                "inputs": inputs,
                "outputs": outputs,
                "transaction_index": data["block_height"],
                "block_time": data["received"]
            }
            return transaction_info
        else:
            return None