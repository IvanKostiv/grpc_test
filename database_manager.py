import os

import psycopg2
from psycopg2.errors import Error

from models import Text


class DatabaseManager:
    def __init__(self):
        self._connection = psycopg2.connect(
            dbname=os.getenv("POSTGRESQL_DB_NAME"),
            host=os.getenv("POSTGRESQL_HOST_NAME"),
            user=os.getenv("POSTGRESQL_USERNAME"),
            password=os.getenv("POSTGRESQL_PASSWORD"),
            port=os.getenv("POSTGRESQL_PORT")
        )

    def add_new_item(self, item: Text) -> tuple[int, str]:
        cursor = self._connection.cursor()
        try:
            cursor.execute(f"INSERT INTO texts(text_id, description) VALUES ('{item.id}', '{item.message}');")
            self._connection.commit()
            status, message = 201, f"Item {item.message} is added!"
        except Error as e:
            print(e)
            status, message = 400, f"Item with id {item.id} is already exist!"
            self._connection.rollback()
        return status, message

    def create_search(self) -> int:
        cursor = self._connection.cursor()
        try:
            cursor.execute(f"INSERT INTO searches(status) VALUES (0);")
            self._connection.commit()
            cursor.execute(f"SELECT search_id from searches ORDER BY search_id DESC LIMIT 1")
            search_id = cursor.fetchone()[0]
        except Error as e:
            print(e)
            search_id = -1

        return search_id

    def get_all_texts(self) -> list[Text]:
        cursor = self._connection.cursor()
        try:
            cursor.execute(f"SELECT * from texts")
            texts = cursor.fetchall()
        except Error as e:
            print(e)
            return []
        return [Text(text[0], text[1]) for text in texts]

    def create_search_to_texts_relationship(self, texts: list[Text], search_id: int) -> None:
        cursor = self._connection.cursor()
        insert_tuple = [(text.id, search_id) for text in texts]
        try:
            cursor.executemany("INSERT INTO searches_texts(text_id, search_id) VALUES (%s,%s)", insert_tuple)
            self._connection.commit()
        except Error as e:
            print(e)
            self._connection.rollback()

    def set_search_status_to_done(self, search_id: int):
        cursor = self._connection.cursor()
        try:
            cursor.execute(f"UPDATE searches SET status = 1 WHERE search_id = {search_id}")
            self._connection.commit()
        except Error as e:
            print(e)
            self._connection.rollback()

    def get_text_by_id(self, text_id: str) -> Text:
        cursor = self._connection.cursor()
        cursor.execute(f"SELECT text_id, description FROM texts WHERE text_id = '{text_id}'")
        word = cursor.fetchone()

        if word is None:
            return Text(id="-1", message=f"Text with text id {text_id} doesn't exist")

        return Text(id=word[0], message=word[1])

    def get_search_results(self, search_id: str) -> list[Text]:
        cursor = self._connection.cursor()
        cursor.execute(f"SELECT status from searches WHERE search_id = {search_id}")
        search_status = cursor.fetchone()

        if search_status is None:
            return [Text(id="-1", message=f"Search process with search id {search_id} doesn't exist")]

        if not search_status:
            return [Text(id="-1", message=f"Search process with search id {search_id} is not completed!")]

        cursor.execute(f"SELECT text_id FROM searches_texts WHERE search_id = {search_id}")
        text_ids = cursor.fetchall()

        return [self.get_text_by_id(text_id[0]) for text_id in text_ids]
