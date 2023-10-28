# simple_pool.py

import multiprocessing
import time

from tasks import get_word_counts

PROCESSES = multiprocessing.cpu_count() - 1


def run():
    print(f"Running with {PROCESSES} processes!")

    start = time.time()
    with multiprocessing.Pool(PROCESSES) as p:
        p.map_async(
            get_word_counts,
            [
                "charles-dickens-oliver-twist.txt",
                "dante-divina-commedia.txt",
                "dostoyevsky-the-idiot.txt",
                "faust-eine-tragodie.txt",
                "herman-bang-tine.txt",
            ],
        )
        # clean up
        p.close()
        p.join()

    print(f"Time taken = {time.time() - start:.10f}")


if __name__ == "__main__":
    run()