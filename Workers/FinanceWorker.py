import threading
import requests
from bs4 import BeautifulSoup


class FinancePriceScheduler(threading.Thread):
    def __init__(self, input_queue, **kwargs):
        super(FinancePriceScheduler, self).__init__(**kwargs)
        self.input_queue = input_queue

    def run(self):
        while True:
            processed_value = self.input_queue.get()
            if processed_value == 'DONE':
                break


class FinanceWorker():
    def __init__(self, symbol, **kwargs):
        self.symbol = symbol.upper()
        self.url = f'https://finance.yahoo.com/quote/{self.symbol}/'
        self.start()

    # def extract_price(self):
    def run(self):
        response = requests.get(self.url)
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




