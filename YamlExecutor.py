import importlib

from multiprocessing import Queue
import yaml
from unicodedata import numeric


class YamlExecutor():
    def __init__(self, pipeline_location):
        self.pipeline_location = pipeline_location
        self.queues = {}
        self.workers = {}

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

            initialization_parameters = {}
            if input_values is not None:
                initialization_parameters['input_values'] = input_values
            if output_queues is not None:
                initialization_parameters['output_queue'] = \
                [self.queues[output_queues] for output_queues in output_queues]
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
        self.join_workers()