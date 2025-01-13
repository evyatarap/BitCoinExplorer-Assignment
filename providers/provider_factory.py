from providers.bitcoin_data_provider import BitcoinDataProvider
from providers.block_cypher_provider import BlockCypherProvider  

class ProviderFactory:
    def __init__(self):
        self.providers = {
            "blockcypher": BlockCypherProvider(),
        }
        
    def get_provider(self, provider_name: str) -> BitcoinDataProvider:
        provider = self.providers.get(provider_name)
        if provider is None:
            raise ValueError(f"Provider '{provider_name}' not found.")
        return provider