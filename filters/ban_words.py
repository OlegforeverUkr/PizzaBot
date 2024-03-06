import os


def read_bad_words() -> set:
    try:
        with open(os.getenv("BAD_WORDS"), "r", encoding="utf-8") as file:
            words = file.read().split()
        return set(words)
    except FileNotFoundError:
        return set()