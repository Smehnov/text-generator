import glob
import pickle
import random


def fit_model(texts_path, model_data_path):
    letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    words = {}
    file_paths = glob.glob(f"./{texts_path}/*.txt")

    for file_path in file_paths:
        file = open(file_path, 'r')
        prev_word = ''
        cur_word = ''

        for line in file:
            for symbol in line.lower():
                if symbol in letters:
                    cur_word += symbol
                else:
                    if cur_word and prev_word:
                        if prev_word in words:
                            if cur_word in words[prev_word]:
                                cur_num = words[prev_word][cur_word]
                                words[prev_word].update({cur_word: (cur_num + 1)})
                            else:
                                words[prev_word].update({cur_word: 1})
                        else:
                            words.update({prev_word: {cur_word: 1}})

                    prev_word = cur_word
                    cur_word = ''
    words_file = open(model_data_path, "wb")
    pickle.dump(words, words_file)


def generate_text(model_data_path, length):
    model_file = open(model_data_path, "rb")
    words = pickle.load(model_file)
    prev_word = random.choice(list(words.keys()))
    s = prev_word

    for i in range(length - 1):
        if prev_word in words:
            next_word = random.choice(list(words[prev_word].keys()))
        else:
            next_word = random.choice(list(words.keys()))
        s += ' ' + next_word
        prev_word = next_word
    print(s)


fit_model("texts", "models/model.data")
generate_text("models/model.data", 5)
