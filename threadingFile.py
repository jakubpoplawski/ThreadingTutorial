import time
from Workers.FinanceWorker import FinanceWorker
from Workers.WikiWorker import WikiWorker

from multiprocessing import Queue

def main():
    symbol_queue = Queue()
    scraping_start_time = time.time()

    wiki_worker = WikiWorker()
    current_workers = []
    for symbol in wiki_worker.get_companies():
        symbol_queue.put(symbol)

    for i in range(len(current_workers)):
        current_workers[i].join()

    print("Extracting took: ", round(time.time() - scraping_start_time, 1))


if __name__ == '__main__':
    main()

