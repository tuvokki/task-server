# https://testdriven.io/blog/developing-an-asynchronous-task-queue-in-python/#redis
# tasks.py

import collections
import json
import os
import sys
import time
import uuid
from pathlib import Path

from nltk.corpus import stopwords

COMMON_WORDS = set(stopwords.words("english"))
BASE_DIR = Path(__file__).resolve(strict=True).parent
DATA_DIR = Path(BASE_DIR).joinpath("books")
OUTPUT_DIR = Path(BASE_DIR).joinpath("output")


def save_file(filename, data):
    random_str = uuid.uuid4().hex
    outfile = f"{filename}_{random_str}.txt"
    with open(Path(OUTPUT_DIR).joinpath(outfile), "w") as outfile:
        outfile.write(data)


def get_word_counts(filename):
    wordcount = collections.Counter()
    # get counts
    with open(Path(DATA_DIR).joinpath(filename), "r") as f:
        try:
            for line in f:
                wordcount.update(line.split())
        except UnicodeDecodeError:
            pass
    for word in set(COMMON_WORDS):
        del wordcount[word]

    # save file
    save_file(filename, json.dumps(dict(wordcount.most_common(20))))

    proc = os.getpid()

    print(f"Processed {filename} with process id: {proc}")


if __name__ == "__main__":
    books = [
        "charles-dickens-oliver-twist.txt",
        "dante-divina-commedia.txt",
        "dostoyevsky-the-idiot.txt",
        "faust-eine-tragodie.txt",
        "herman-bang-tine.txt",
    ]

    start = time.time()

    if len(sys.argv) < 1:
        get_word_counts(sys.argv[1])
    else:
        for book in books:
            # print(f"Book analysis on {book}")
            book_start = time.time()
            get_word_counts(book)
            # print(f"Time taken = {time.time() - book_start:.10f}")

    print(f"Time taken = {time.time() - start:.10f}")
