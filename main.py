from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
from providers.provider_factory import ProviderFactory
from providers.bitcoin_data_provider import AddressInfo, TransactionInfo
from redis_db_conn import RedisDBConn
import utils
import logging
import os
import json
from dotenv import load_dotenv, find_dotenv

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info("Starting Bitcoin Explorer API")

# Load environment variables from .env file
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)
    logger.debug(f"Loaded environment variables from {dotenv_path}")
else:
    logger.debug(".env file not found. Proceeding without loading environment variables.")


class SharedResources:
   bitcoin_data_provider = None
   db_conn = None

@asynccontextmanager
async def lifespan(app: FastAPI):
      try:
         provider_factory = ProviderFactory()
         SharedResources.bitcoin_data_provider = provider_factory.get_provider("blockcypher")
         logger.info("Provider initialized successfully")
        
         SharedResources.db_conn = RedisDBConn(
            host=os.getenv("REDIS_HOST"),
            port=int(os.getenv("REDIS_PORT")),
            access_key=os.getenv("REDIS_ACCESS_KEY"))
         
         if not SharedResources.db_conn.connect():
            raise RuntimeError("Failed to connect to Redis")
         
         yield
      except Exception as e:
         logger.error(f"Failed to initialize provider: {e}")
         raise RuntimeError("Failed to initialize provider") from e

app = FastAPI(title="Bitcoin Explorer", 
               version="1.0.0", 
               description="API for providing information on Bitcoin addresses and transactions.", 
               lifespan=lifespan)

def get_provider():
    return SharedResources.bitcoin_data_provider

def get_db_conn():
    return SharedResources.db_conn  


@app.get("/address/{bitcoin_address}", response_model=AddressInfo, summary="This endpoint receives a Bitcoin address and returns the balance and transaction count for that address.")
def get_address_info(bitcoin_address: str, provider = Depends(get_provider), db_conn = Depends(get_db_conn)):
   if not utils.is_valid_bitcoin_address(bitcoin_address):
      raise HTTPException(status_code=400, detail="Invalid Bitcoin address")

   # Check if the address info is in the cache
   cached_address_info = db_conn.get(bitcoin_address)
   if cached_address_info:
      logger.debug(f"Retrieved address info for {bitcoin_address} from cache")
      return json.loads(cached_address_info)
    
   # If not in cache, fetch from provider
   address_info = provider.get_address_info(bitcoin_address)
   if address_info:
      logger.debug(f"Retrieved address info for {bitcoin_address} from provider")
      # Cache the address info with a TTL of 1 hour (3600 seconds)
      db_conn.set(bitcoin_address, json.dumps(address_info), ttl=3600)
      return address_info
   
   raise HTTPException(status_code=404, detail="Address information could not be retrieved")

@app.get("/transaction/{transaction_hash}", response_model=TransactionInfo, summary="This endpoint receives a transaction hash and returns detailed information about the transaction.")    
def get_transaction_info(transaction_hash: str, provider = Depends(get_provider), db_conn = Depends(get_db_conn)):
   if not utils.is_valid_transaction_hash(transaction_hash):
      raise HTTPException(status_code=400, detail="Invalid transaction hash")
    
   # Check if the transaction info is in the cache
   cached_transaction_info = db_conn.get(transaction_hash)
   if cached_transaction_info:
      logger.debug(f"Retrieved transaction info for {transaction_hash} from cache")
      return json.loads(cached_transaction_info)
   
   transaction_info = provider.get_transaction_info(transaction_hash)
   if transaction_info:
      logger.debug(f"Retrieved transaction info for {transaction_hash} from provider")
      
      if(transaction_info["transaction_index"] == -1):
         # Cache the transaction info with TTL of 10 minutes, if the transaction is unconfirmed.
         db_conn.set(transaction_hash, json.dumps(transaction_info), ttl=600)
      else:
         # Cache the transaction info indefinitely, if the transaction is confirmed.
         db_conn.set(transaction_hash, json.dumps(transaction_info))

      return transaction_info
   raise HTTPException(status_code=404, detail="Transaction information could not be retrieved")