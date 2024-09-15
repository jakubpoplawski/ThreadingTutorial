import threading


class SquaredSumWorker(threading.Thread):
    def __init__(self, n, **kwargs):
        self.n = n
        super(SquaredSumWorker, self).__init__(**kwargs)
        self.start()

    def sum_of_squares(self):
        sum_sq = 0
        for i in range(self.n):
            sum_sq += i ** 2
        print(sum_sq)

    def run(self):
        self.sum_of_squares()

