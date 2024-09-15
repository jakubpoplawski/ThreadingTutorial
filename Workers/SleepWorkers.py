import threading
import time


class SleepWorker(threading.Thread):
    def __init__(self, seconds, **kwargs):
        self.seconds = seconds
        super(SleepWorker, self).__init__(**kwargs)
        self.start()

    def sleep_some(self):
        time.sleep(self.seconds)

    def run(self):
        self.sleep_some()