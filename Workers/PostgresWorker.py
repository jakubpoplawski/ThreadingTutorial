import os
import random
import threading
import time
from queue import Empty


from sqlalchemy import create_engine
from sqlalchemy.sql import text


class PostgresScheduler(threading.Thread):
    def __init__(self, input_queue, output_queue=None, **kwargs):
        # if 'output_queue' in kwargs:
        #     kwargs.pop('output_queue')
        super(PostgresScheduler, self).__init__(**kwargs)
        self.input_queue = input_queue
        self.start()

    def run(self):
        while True:
            try:
                processed_value = self.input_queue.get(timeout=20)
            except Empty:
                print("Timeout reached in PostgresWorker.")
                break
            if processed_value == 'DONE':
                break
            try:
                symbol, price, extracted_time, fin_thread_id = processed_value
            except ValueError:
                print(f"Processing error values: {processed_value}")
            postgres_worker = PostgresWorker(symbol, price,
                                             extracted_time, fin_thread_id)
            postgres_worker.insert_into_database()



class PostgresWorker():
    def __init__(self, symbol, price, extracted_time, fin_thread_id, **kwargs):
        self.symbol = symbol
        self.price = price
        self.extracted_time = extracted_time
        self.fin_thread_id = fin_thread_id
        self.postgres_user = os.environ.get('postgres_user')
        self.postgres_password = os.environ.get('postgres_password')
        self.postgres_host = os.environ.get('postgres_host')
        self.postgres_database = os.environ.get('postgres_database')
        self.postgres_engine = create_engine(
            f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}/{self.postgres_database}")


    def create_insert_query(self):
        sql_query = """INSERT INTO public.stock_prices (stock_name, stock_price, extracted_time, thread_id) 
                        VALUES (:symbol, :price, :extracted_time, :fin_thread_id)"""
        return sql_query


    def insert_into_database(self):
        insert_query = self.create_insert_query()

        with self.postgres_engine.connect() as sql_connection:
            sql_connection.execute(
                text(insert_query), {'symbol': self.symbol,
                                    'price': self.price,
                                    'extracted_time': self.extracted_time,
                                    'fin_thread_id': self.fin_thread_id})
            sql_connection.commit()
