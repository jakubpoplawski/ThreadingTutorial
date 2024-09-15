import random
import threading
import time

import requests
from bs4 import BeautifulSoup


class FinancePriceScheduler(threading.Thread):
    def __init__(self, input_queue, **kwargs):
        super(FinancePriceScheduler, self).__init__(**kwargs)
        self.input_queue = input_queue
        self.start()

    def run(self):
        while True:
            processed_value = self.input_queue.get()
            if processed_value == 'DONE':
                break
            finance_worker = FinanceWorker(symbol=processed_value)
            retrieved_price = finance_worker.extract_price()
            print(retrieved_price)
            time.sleep(random.random())


class FinanceWorker():
    def __init__(self, symbol, **kwargs):
        self.symbol = symbol.upper()
        self.headers = {"User-Agent":
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            + "AppleWebKit/537.36 (KHTML, like Gecko) "
                            +  "Chrome/92.0.4515.159 Safari/537.36",}
        self.url = f'https://finance.yahoo.com/quote/{self.symbol}/'


    def extract_price(self):
        response = requests.get(self.url, headers=self.headers)
        time.sleep(5)
        if response.status_code != 200:
            print('Page unavailable.')
            pass
        else:
            soup = BeautifulSoup(response.text, 'lxml')
            price = soup.find(
                'fin-streamer', class_="livePrice yf-mgkamr").text
            try:
                return float(price)
            except ValueError:
                print('Caught value is not a number.')

