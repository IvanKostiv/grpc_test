import asyncio
import os
import threading

import grpc
from dotenv import load_dotenv
from fuzzywuzzy import fuzz

from database_manager import DatabaseManager
from models import Text
from search_pb2 import SearchResult, SearchItemsResponse, GetSearchResultsRequest, SearchItemsRequest, \
    GetSearchResultsResponse, AddItemResponse, AddItemRequest
from search_pb2_grpc import SimilaritySearchServiceServicer, add_SimilaritySearchServiceServicer_to_server


SIMILARITY_RATIO = 75


class SearchServicer(SimilaritySearchServiceServicer):
    def __init__(self):
        self.database_manager = DatabaseManager()
        self.task_queue = asyncio.Queue()

    async def SearchItems(self, request: SearchItemsRequest, context) -> SearchItemsResponse:
        search_id = self.database_manager.create_search()

        # put parameters for searching in queue
        await self.task_queue.put((self.database_manager, search_id, request))
        # create worker for searching
        task = asyncio.create_task(search_worker(self.task_queue))
        # run worker in new thread
        threading.Thread(target=self.__run_search_task, args=(task,))

        return SearchItemsResponse(search_id=str(search_id))

    def GetSearchResults(self, request: GetSearchResultsRequest, context) -> GetSearchResultsResponse:
        search_results = self.database_manager.get_search_results(request.search_id)
        return GetSearchResultsResponse(
            results=[SearchResult(id=text.id, description=text.message) for text in search_results]
        )

    def AddItem(self, request: AddItemRequest, context) -> AddItemResponse:
        word = Text(id=request.id, message=request.description)
        status, message = self.database_manager.add_new_item(word)
        return AddItemResponse(status=status, message=message)

    def __run_search_task(self, task) -> None:
        task.cancel()
        asyncio.gather(task)


async def serve():
    server = grpc.aio.server()
    add_SimilaritySearchServiceServicer_to_server(SearchServicer(), server)
    server.add_insecure_port(f'{os.getenv("GRPC_HOST")}:{os.getenv("GRPC_PORT")}')
    await server.start()
    await server.wait_for_termination()


async def search_worker(queue: asyncio.Queue) -> None:
    while True:
        database_manager, search_id, search_request = await queue.get()
        await search(database_manager, search_id, search_request)
        queue.task_done()


async def search(database_manager: DatabaseManager, search_id: int, search_request: SearchItemsRequest) -> None:
    texts = database_manager.get_all_texts()
    results = [text for text in texts if fuzz.ratio(text.message, search_request.query) > SIMILARITY_RATIO]
    database_manager.create_search_to_texts_relationship(results, search_id)
    database_manager.set_search_status_to_done(search_id)


if __name__ == '__main__':
    load_dotenv()
    asyncio.get_event_loop().run_until_complete(serve())
