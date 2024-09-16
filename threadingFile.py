import time
from Workers.FinanceWorker import FinancePriceScheduler
from Workers.WikiWorker import WikiWorker
from Workers.PostgresWorker import PostgresScheduler

from multiprocessing import Queue

def main():
    symbol_queue = Queue()
    postgres_queue = Queue()

    scraping_start_time = time.time()

    wiki_worker = WikiWorker()

    finance_price_threads = []
    number_of_finance_workers = 5

    for i in range(number_of_finance_workers):
        finance_price_scheduler = FinancePriceScheduler(
            input_queue=symbol_queue, output_queue=postgres_queue)
        finance_price_threads.append(finance_price_scheduler)

    postgres_threads = []
    number_of_postgres_workers = 2

    for i in range(number_of_postgres_workers):
        postgres_scheduler = PostgresScheduler(input_queue=postgres_queue)
        postgres_threads.append(postgres_scheduler)

    for symbol in wiki_worker.get_companies():
        symbol_queue.put(symbol)

    for thread_instance in range(len(finance_price_threads)):
        symbol_queue.put('DONE')

    for i in range(len(finance_price_threads)):
        finance_price_threads[i].join()

    print("Extracting took: ", round(time.time() - scraping_start_time, 1))


if __name__ == '__main__':
    main()

