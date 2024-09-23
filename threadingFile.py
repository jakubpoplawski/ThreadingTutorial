import time
import os
from dotenv import load_dotenv
from multiprocessing import Queue

from Workers.FinanceWorker import FinancePriceScheduler
from Workers.WikiWorker import WikiWorker
from Workers.PostgresWorker import PostgresScheduler
from YamlExecutor import YamlExecutor

def main():
    load_dotenv()

    yaml_executor = YamlExecutor(
        pipeline_location='Pipelines/wiki_fin_scraper.yaml')

    yaml_executor.process_pipeline()

#    symbol_queue = Queue()
#    postgres_queue = Queue()

    scraping_start_time = time.time()

    wiki_worker = WikiWorker()

    # finance_price_threads = []
    # number_of_finance_workers = 4
    #
    # for i in range(number_of_finance_workers):
    #     finance_price_scheduler = FinancePriceScheduler(
    #         input_queue=symbol_queue, output_queue=[postgres_queue])
    #     finance_price_threads.append(finance_price_scheduler)

    # postgres_threads = []
    # number_of_postgres_workers = 2
    #
    # for i in range(number_of_postgres_workers):
    #     postgres_scheduler = PostgresScheduler(input_queue=postgres_queue)
    #     postgres_threads.append(postgres_scheduler)

    symbol_counter = 0
    for symbol in wiki_worker.get_companies():
        yaml_executor.queues['SymbolQueue'].put(symbol)
        symbol_counter += 1
        if symbol_counter >= 5:
            break

    for thread_instance in range(20):
        yaml_executor.queues['SymbolQueue'].put('DONE')

    yaml_executor.join_workers()

    # for i in range(len(finance_price_threads)):
    #     finance_price_threads[i].join()
    #
    # for i in range(len(postgres_threads)):
    #     postgres_threads[i].join()

    print("Extracting took: ", round(time.time() - scraping_start_time, 1))


if __name__ == '__main__':
    main()
