import json

from word_forms.word_forms import get_word_forms
from word_forms.lemmatizer import lemmatize

def recurse(dict):
    result = []
    for key in dict:
        result.append(key)
        result.extend(recurse(dict[key]))
    return result

def parse_he_dict(dic, en_klld):
    f = open('/home/aviad/files/programming/projects/python/WordDumb/klld/dict-en-he.json', 'r')
    dictionary_json = json.loads(f.read())
    f.close()

    dictionary = []
    dictionary_data = []
    for entry in dictionary_json:
        dictionary.append(entry['translated'])
        dictionary_data.append(entry)

    all = 0
    good = 0
    for ww_word in en_klld:
        all += 1
        original = ww_word
        if not ww_word in dictionary:
            try:
                # Try lemmatizing
                ww_word = lemmatize(ww_word)
            except ValueError:
                continue # This is not a real word...

            if not ww_word in dictionary:
                continue # If still does not help - continue...
        
        good += 1
        if good % 1000 == 0:
            print(good)
        entry = dictionary_data[dictionary.index(ww_word)]
        hebrew  = entry['translation']
        dic[original].append((', '.join(hebrew), hebrew[0]))

    print(dic)

    print(f'Compared to wordwise: {good} / {len(en_klld)} ({int(good / len(en_klld) * 100)})%')
