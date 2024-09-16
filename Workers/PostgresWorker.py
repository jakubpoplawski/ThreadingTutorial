import os
import random
import threading
import time
from sqlalchemy import create_engine
from sqlalchemy.sql import text

class PostgresScheduler(threading.Thread):
    def __init__(self, input_queue, **kwargs):
        super(PostgresScheduler, self).__init__(**kwargs)
        self.input_queue = input_queue
        self.start()

    def run(self):
        while True:
            processed_value = self.input_queue.get()
            if processed_value == 'DONE':
                break
            symbol, price, extracted_time = processed_value
            postgresWorker = PostgresWorker(symbol, price, extracted_time)
            postgresWorker.insert_into_database()



class PostgresWorker():
    def __init__(self, symbol, price, extracted_time, **kwargs):
        self.symbol = symbol
        self.price = price
        self.extracted_time = extracted_time
        self.postgres_user = os.environ.get('postgres_user')
        self.postgres_password = os.environ.get('postgres_password')
        self.postgres_host = os.environ.get('postgres_host')
        self.postgres_database = os.environ.get('postgres_database')
        self.postgres_engine = create_engine(
            f"postgres://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}/{self.postgres_database}")


    def create_insert_query(self):
        sql_query = """INSERT INTO stock_prices (stock_name, stock_price, extracted_time) 
                        VALUES (:symbol, :price, :extracted_time)"""
        return sql_query


    def insert_into_database(self):
        insert_query = self.create_insert_query()

        with self.postgres_engine.connect() as sql_connection:
            sql_connection.execute(
                text(insert_query, {'symbol': self.symbol,
                                    'price': self.price,
                                    'extracted_time': self.extracted_time}))
