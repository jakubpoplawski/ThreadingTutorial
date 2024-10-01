import importlib


import threading
import time

from multiprocessing import Queue
import yaml



class YamlExecutor(threading.Thread):
    def __init__(self, pipeline_location, **kwargs):
        super(YamlExecutor, self).__init__()
        self.pipeline_location = pipeline_location
        self.queues = {}
        self.workers = {}
        self.queue_consumers = {}
        self.downstream_queues = {}
        self.start()

    def load_pipeline(self):
        with open(self.pipeline_location, 'r') as readFile:
            self.yaml_data = yaml.safe_load(readFile)

    def initialize_queues(self):
        for queue in self.yaml_data['queues']:
            queue_name = queue['name']
            self.queues[queue_name] = Queue()

    def initialize_workers(self):
        for worker in self.yaml_data['workers']:
            WorkerClass = getattr(importlib.import_module(worker['location']),
                                  worker['class'])
            input_queue = worker.get('input_queue')
            output_queues = worker.get('output_queues')
            input_values = worker.get('input_values')
            worker_name = worker['name']

            instances_number = worker.get('instances', 1)

            self.downstream_queues[worker_name] = output_queues
            if input_queue is not None:
                self.queue_consumers[input_queue] = instances_number

            initialization_parameters = {}
            if input_values is not None:
                initialization_parameters['input_values'] = input_values
            if output_queues is not None:
                initialization_parameters['output_queue'] = \
                [self.queues[output_queue] for output_queue in output_queues]
            if input_queue is not None:
                initialization_parameters['input_queue'] = \
                self.queues[input_queue]

            self.workers[worker_name] = []
            for i in range(instances_number):
                self.workers[worker_name].append(
                    WorkerClass(**initialization_parameters))

    def join_workers(self):
        for worker_name in self.workers:
            for worker_thread in self.workers[worker_name]:
                worker_thread.join()

    def process_pipeline(self):
        self.load_pipeline()
        self.initialize_queues()
        self.initialize_workers()
        #self.join_workers()

    def run(self):
        self.process_pipeline()

        while True:
            total_workers_alive = 0
            worker_statistics = []
            workers_to_delete = []
            for worker_name in self.workers:
                total_workers_threads_alive = 0
                for worker_thread in self.workers[worker_name]:
                    if worker_thread.is_alive():
                        total_workers_threads_alive += 1
                total_workers_alive += total_workers_threads_alive
                if total_workers_threads_alive == 0:
                    if self.downstream_queues[worker_name] is not None:
                        for output_queue in self.downstream_queues[worker_name]:
                            number_of_consumers = self.queue_consumers[output_queue]
                            for i in range(number_of_consumers):
                                self.queues[output_queue].put('DONE')

                    workers_to_delete.append(worker_name)

                worker_statistics.append([worker_name, total_workers_threads_alive])
            print(worker_statistics)
            if total_workers_alive == 0:
                break

            for worker_name in workers_to_delete:
                del self.workers[worker_name]


            time.sleep(5)