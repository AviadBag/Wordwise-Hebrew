import json
from nltk.corpus import wordnet as wn

from nltk.corpus import wordnet as wn

# Just to make it a bit more readable
WN_NOUN = 'n'
WN_VERB = 'v'
WN_ADJECTIVE = 'a'
WN_ADJECTIVE_SATELLITE = 's'
WN_ADVERB = 'r'
WN_ALL = [WN_NOUN, WN_VERB, WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE, WN_ADVERB]

def convert(word, from_pos, to_pos):    
    """ Transform words given from/to POS tags """

    synsets = wn.synsets(word, pos=from_pos)

    # Word not found
    if not synsets:
        return []

    # Get all lemmas of the word (consider 'a'and 's' equivalent)
    lemmas = []
    for s in synsets:
        for l in s.lemmas():
            if s.name().split('.')[1] == from_pos or from_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE) and s.name().split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE):
                lemmas += [l]

    # Get related forms
    derivationally_related_forms = [(l, l.derivationally_related_forms()) for l in lemmas]

    # filter only the desired pos (consider 'a' and 's' equivalent)
    related_noun_lemmas = []

    for drf in derivationally_related_forms:
        for l in drf[1]:
            if l.synset().name().split('.')[1] == to_pos or to_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE) and l.synset().name().split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE):
                related_noun_lemmas += [l]

    # Extract the words from the lemmas
    words = [l.name() for l in related_noun_lemmas]
    len_words = len(words)

    # Build the result in the form of a list containing tuples (word, probability)
    result = [(w, float(words.count(w)) / len_words) for w in set(words)]
    result.sort(key=lambda w:-w[1])

    # return all the possibilities sorted by probability
    return result

def parse_he_dict(dic, en_klld):
    f = open('/home/aviad/files/programming/projects/python/WordDumb/klld/dict-en-he.json', 'r')
    dictionary_json = json.loads(f.read())
    f.close()

    all = 0
    good = 0
    for t in dictionary_json:
        english = t['translated']
        hebrew  = t['translation']
        all += 1
    
        word = None
        if english in en_klld:
            word = english
        else: # We have to find the closest form
            # Get all possible options
            options = []
            for from_type in WN_ALL:
                options.extend(convert(english, from_type, WN_NOUN))
            
            # Sort according to the most probable word
            options.sort(key=lambda option: (1-option[1]))

            # Filter the most unlikelyest words
            options = filter(lambda option: option[1] > 0.4, options)

            for option in options:
                if option[0] in en_klld:
                    word = option[0]
                    found = True
                    break
        
        if word != None:
            good += 1
            dic[english].append((', '.join(hebrew), hebrew[0]))

    print(f'Compared to full dictionary: {good} / {all} ({int(good / all * 100)})%')
    print(f'Compared to wordwise: {good} / {len(en_klld)} ({int(good / len(en_klld) * 100)})%')