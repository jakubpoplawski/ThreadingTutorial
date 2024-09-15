import time
import threading

def sum_of_squares(n):
    sum_sq = 0
    for i in range(n):
        sum_sq += i ** 2
    print(sum_sq)


def sleep_some(seconds):
    time.sleep(seconds)


def main():
    calc_start_time = time.time()

    current_threads = []
    for i in range(5):
        maximum_val = (i + 1) * 10000000
        t = threading.Thread(target=sum_of_squares, args=(maximum_val,), daemon=True)
        t.start()
        current_threads.append(t)

    for i in range(len(current_threads)):
        current_threads[i].join()

    print("Calc time took: ", round(time.time() - calc_start_time, 1))

    sleep_start_time = time.time()

    current_threads = []
    for i in range(1, 6):
        seconds = i
        t = threading.Thread(target=sleep_some, args=(seconds,))
        t.start()
        current_threads.append(t)

    for i in range(len(current_threads)):
        current_threads[i].join()

    print("Sleep took: ", round(time.time() - sleep_start_time, 1))


if __name__ == '__main__':
    main()

