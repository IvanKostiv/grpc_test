# Installation
## PostgreSQL
Open command prompt and run command to create database and schema
```commandline
createdb -U <POSTGRES_USER[postgres]> <DB_NAME[reply_io_test]>)
psql -U <POSTGRES_USER[postgres]> <DB_NAME[reply_io_test]> < db.sql
```
## Python
1. Python version `3.9.3`
2. Run command to install all necessary python packages
```commandline
pip install -r requirements.txt
```
3. Modify .env file in the root of repository and fill it with these variables:
```dotenv
POSTGRESQL_USERNAME=<POSTGRES_USER> # postgres
POSTGRESQL_PASSWORD=<POSTGRES_PASSWORD>
POSTGRESQL_HOST_NAME=<POSTGRES_USERNAME>
POSTGRESQL_DB_NAME=<POSTGRES_DB_NAME> # reply_io_test
POSTGRESQL_PORT=<POSTGRES_PORT>

GRPC_HOST=<GRPC_HOST>
GRPC_PORT=<GRPC_PORT>
```
# Run
1. To run server, run the command
```commandline
python server.py
```
2. To run client, run the command
```commandline
uvicorn client:app
```
# Usage
1. Open your web browser with address http://127.0.0.1:8000/
2. You can use `add_item` route to add new item to database by providing  `id` and `description`
3. You can use `search_items` route to  search for similar items in the database based on the `query`
4. You can user `get_search_results` route to get search results associated with the given `search_id` from the database