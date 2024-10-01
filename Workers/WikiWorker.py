import requests
import threading

from bs4 import BeautifulSoup



class WikiWorkerScheduler(threading.Thread):
    def __init__(self, output_queue, input_values, **kwargs):
        self.input_values = input_values

        temp_queue = output_queue
        if type(temp_queue) != list:
            temp_queue = [temp_queue]
        self.output_queues = temp_queue
        super(WikiWorkerScheduler, self).__init__(**kwargs)
        self.start()

    def run(self):
        for input_value in self.input_values:
            wiki_worker = WikiWorker(input_value)

            symbol_counter = 0
            for symbol in wiki_worker.get_companies():
                for output_queue in self.output_queues:
                    output_queue.put(symbol)
                    symbol_counter += 1
                    if symbol_counter >= 5:
                        break

        # for output_queue in self.output_queues:
        #     for i in range(20):
        #         output_queue.put('DONE')


class WikiWorker():
    def __init__(self, url):
        self.url = url

    @staticmethod
    def extract_companies(page_html):
        soup = BeautifulSoup(page_html, 'lxml')
        table = soup.find(id='constituents')
        table_rows = table.find_all('tr')
        for table_row in table_rows[1:]:
            symbol = table_row.find('td').text.strip('\n')
            yield symbol

    def get_companies(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            print('Page unavailable.')
            return []
        else:
            yield from self.extract_companies(response.text)



