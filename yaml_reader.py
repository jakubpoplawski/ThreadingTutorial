import importlib

from multiprocessing import Queue
import yaml
from unicodedata import numeric


class YamlReader():
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
            WorkerClass = getattr(importlib.import_module(worker['location']), worker['class'])
            input_queue = worker.get('input_queue')
            output_queues = worker.get('output_queues')
            worker_name = worker['name']
            instances_number = worker.get('instances', 1)

            initialization_parameters = {
                'input_queue': self.queues[input_queue] if not None else None,
                'output_queues': [self.queues[output_queues] \
                                   for output_queue in output_queues] \
                                    if output_queues is not None else None
            }

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