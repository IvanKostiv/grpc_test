import os

import grpc
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from search_pb2_grpc import SimilaritySearchServiceStub
from search_pb2 import GetSearchResultsRequest, SearchItemsRequest, AddItemRequest

load_dotenv()

GRPC_CONNECTION = f'{os.getenv("GRPC_HOST")}:{os.getenv("GRPC_PORT")}'
app = FastAPI()


class Item(BaseModel):
    id: str
    description: str


class AddItemResponseAPI(BaseModel):
    status: int
    message: str


class SearchItemsResponseAPI(BaseModel):
    search_id: str


class GetSearchResultResponseAPI(BaseModel):
    results: list[Item]


@app.get("/", include_in_schema=False)
def home_to_docs():
    return RedirectResponse("/docs")


@app.post("/add_item", response_model=AddItemResponseAPI)
async def add_item(item: Item):
    with grpc.insecure_channel(GRPC_CONNECTION) as channel:
        stub = SimilaritySearchServiceStub(channel)
        response = stub.AddItem(AddItemRequest(id=item.id, description=item.description))
        return AddItemResponseAPI(status=response.status, message=response.message)


@app.get("/search_items", response_model=SearchItemsResponseAPI)
async def search_items(query: str):
    with grpc.insecure_channel(GRPC_CONNECTION) as channel:
        stub = SimilaritySearchServiceStub(channel)
        response = stub.SearchItems(SearchItemsRequest(query=query))
        return SearchItemsResponseAPI(search_id=response.search_id)


@app.get("/get_search_results/{search_id}", response_model=GetSearchResultResponseAPI)
async def get_search_result(search_id: int):
    with grpc.insecure_channel(GRPC_CONNECTION) as channel:
        stub = SimilaritySearchServiceStub(channel)
        response = stub.GetSearchResults(GetSearchResultsRequest(search_id=str(search_id)))
        return GetSearchResultResponseAPI(
            results=[Item(id=item.id, description=item.description) for item in response.results]
        )
