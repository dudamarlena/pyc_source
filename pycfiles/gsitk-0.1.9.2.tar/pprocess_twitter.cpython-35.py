# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oaraque/git/gsi/gsitk/gsitk/preprocess/pprocess_twitter.py
# Compiled at: 2017-02-16 10:30:18
# Size of source mod 2**32: 2199 bytes
"""
preprocess-twitter.py

python preprocess-twitter.py "Some random text with #hashtags, @mentions and http://t.co/kdjfkdjf (links). :)"

Script for preprocessing tweets by Romain Paulus
with small modifications by Jeffrey Pennington
with translation to Python by Motoki Wu

Translation of Ruby script to create features for GloVe vectors for Twitter data.
http://nlp.stanford.edu/projects/glove/preprocess-twitter.rb
"""
import sys, re
FLAGS = re.MULTILINE | re.DOTALL

def hashtag(text):
    text = text.group()
    hashtag_body = text[1:]
    if hashtag_body.isupper():
        result = '<hashtag> {} <allcaps>'.format(hashtag_body)
    else:
        result = '<hastag> {}'.format(hashtag_body)
    return result


def allcaps(text):
    text = text.group()
    return text.lower() + ' <allcaps>'


def tokenize(text):
    eyes = '[8:=;]'
    nose = "['`\\-]?"

    def re_sub(pattern, repl):
        return re.sub(pattern, repl, text, flags=FLAGS)

    text = re_sub('https?:\\/\\/\\S+\\b|www\\.(\\w+\\.)+\\S*', '<url>')
    text = re_sub('/', ' / ')
    text = re_sub('@\\w+', '<user>')
    text = re_sub('{}{}[)dD]+|[)dD]+{}{}'.format(eyes, nose, nose, eyes), '<smile>')
    text = re_sub('{}{}p+'.format(eyes, nose), '<lolface>')
    text = re_sub('{}{}\\(+|\\)+{}{}'.format(eyes, nose, nose, eyes), '<sadface>')
    text = re_sub('{}{}[\\/|l*]'.format(eyes, nose), '<neutralface>')
    text = re_sub('<3', '<heart>')
    text = re_sub('[-+]?[.\\d]*[\\d]+[:,.\\d]*', '<number>')
    text = re_sub('#\\S+', hashtag)
    text = re_sub('([!?.]){2,}', '\\1 <repeat>')
    text = re_sub('\\b(\\S*?)(.)\\2{2,}\\b', '\\1\\2 <elong>')
    text = re_sub('([A-Z]){2,}', allcaps)
    return text.lower()


if __name__ == '__main__':
    _, text = sys.argv
    if text == 'test':
        text = 'I TEST alllll kinds of #hashtags and #HASHTAGS, @mentions and 3000 (http://t.co/dkfjkdf). w/ <3 :) haha!!!!!'
    tokens = tokenize(text)
    print(tokens)