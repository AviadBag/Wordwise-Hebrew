from bs4 import BeautifulSoup
import re

cleaner1 = re.compile('[a-z]+(\[.*\])')
cleaner2 = re.compile('[a-z]+')

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def parse_he_dict(rawml_path, dic, en_klld):
    f = open(rawml_path, 'r')
    html = f.read()
    f.close()

    parsed_html = BeautifulSoup(html, features="lxml")
    body = parsed_html.body
    print('[+] Done parsing dictionary... Now iterating words')
    
    for word, definition in chunks(body.contents[2:], 2):
        word = word.strip()
        definition = definition.text
        definition = cleaner1.sub('', definition)
        definition = cleaner2.sub('', definition)
        short_definition = definition.split(',')[0]
        print(f'word: {word}, definition: {definition}, short: {short_definition}')
        if word in en_klld:
            dic[word].append((definition, short_definition))
    print('[+] Finished iterating words... Creating klld file')