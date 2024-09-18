import random
import threading

import datetime
import time

import requests
from bs4 import BeautifulSoup


class FinancePriceScheduler(threading.Thread):
    def __init__(self, input_queue, output_queue, **kwargs):
        super(FinancePriceScheduler, self).__init__(**kwargs)
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.start()

    def run(self):
        while True:
            processed_value = self.input_queue.get()
            if processed_value == 'DONE':
                if self.output_queue is not None:
                    self.output_queue.put('None')
                break
            finance_worker = FinanceWorker(symbol=processed_value)
            retrieved_price = finance_worker.extract_price()
            if self.output_queue is not None:
                output_values = (processed_value,
                                 retrieved_price,
                                 datetime. datetime. now(datetime. UTC))
                self.output_queue.put(output_values)
            time.sleep(random.random())


class FinanceWorker():
    def __init__(self, symbol, **kwargs):
        self.symbol = symbol.upper()
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}
        self.url = f'https://finance.yahoo.com/quote/{self.symbol}/'


    def extract_price(self):
        response = requests.get(self.url, headers=self.headers)
        time.sleep(random.random() * 2)
        if response.status_code != 200:
            print('Page unavailable.')
            pass
        else:
            soup = BeautifulSoup(response.text, 'lxml')
            read_price = soup.find(
                'fin-streamer', class_="livePrice yf-mgkamr").text
            cleaned_price = read_price.replace(",", "")
            try:
                return float(cleaned_price)
            except ValueError:
                print('Caught value is not a number.')

fw = FinanceWorker('mmm')
print(fw.extract_price())