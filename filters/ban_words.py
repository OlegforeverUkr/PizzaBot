def read_bad_words() -> set:
    try:
        with open("C:\\Users\\Oleg\\PycharmProjects\\BotStore\\bad_words.txt", "r", encoding="utf-8") as file:
            words = file.read().split()
        return set(words)
    except FileNotFoundError:
        print("File 'bad_words.txt' not found.")
        return set()