# Bitcoin Explorer API

The Bitcoin Explorer API is a FastAPI-based application that provides information on Bitcoin addresses and transactions. It leverages third-party providers to fetch data and uses Redis for caching to improve performance and reduce the load on external services.

## Features

- **Bitcoin Transactions**: The API caches confirmed transactions indefinitely. Unconfirmed transactions are cached for 10 minutes.
- **Bitcoin Address Data**: The API caches address data for one hour.

## Running and Configuring the Application

### Setting Up Environment Variables:

To configure the application, ensure the following environment variables are set:

- REDIS_HOST: The endpoint address of your Redis server.
- REDIS_PORT: The port number used to connect to the Redis server.
- REDIS_ACCESS_KEY: The access key or password for your Redis server.

### Launching the Application:
Once the environment is configured, start the application with the command:

```sh
uvicorn main:app --host 0.0.0.0 --port 8000
```
