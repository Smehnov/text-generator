import glob
import pickle
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mode', help='Text-generator mode(train or generate)')
parser.add_argument('-t', '--texts-folder', help='Path to folder with texts(for training model)')
parser.add_argument('-d', '--model-data', help='Path to model')
parser.add_argument('-l', '--length', help='Length of generating text')
args = vars(parser.parse_args())



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

if args['mode'] == 'train':
    if args['texts_folder'] and args['model_data']:
        fit_model(args['texts_folder'], args['model_data'])
    else:
        print("Texts folder or model data path aren't set")
elif args['mode'] == 'generate':
    if args['model_data']:
        if args['length']:
            generate_text(args['model_data'], int(args['length']))
        else:
            generate_text(args['model_data'], 5)
    else:
        print("Path to model data isn't set")

