# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/buzzword/create.py
# Compiled at: 2019-08-21 11:24:46
# Size of source mod 2**32: 2473 bytes
"""
buzzword: make a workspace for buzzword in the current directory

Usage: python -m buzzword.create <name>

Once a workspace is defined, you can cd in there and run buzzword.

You can modify the various config and data files as you see fit.
"""
import os, sys
from buzz.corpus import Corpus
NAME = sys.argv[(-1)]
FULLNAME = os.path.abspath(NAME)
CORPUS_PATH = os.path.join(NAME, 'example')
print('Making a new workspace at {}'.format(FULLNAME))
ENV = '\n# .env example for deploying buzzword\n# comment out keys you are not using\nBUZZWORD_CORPORA_FILE=corpora.json\nBUZZWORD_ROOT={}\nBUZZWORD_LOAD=true\nBUZZWORD_TITLE=buzzword\nBUZZWORD_DEBUG=false\n# BUZZWORD_MAX_DATASET_ROWS=999999\nBUZZWORD_DROP_COLUMNS=parse,text\nBUZZWORD_PAGE_SIZE=25\nBUZZWORD_TABLE_SIZE=2000,200\nBUZZWORD_ADD_GOVERNOR=false\n'.format(FULLNAME)
CORPORA = '\n{{\n  "Example corpus: joke": {{\n    "slug": "jokes",\n    "path": "{}",\n    "desc": "Sample corpus with speaker names and metadata",\n    "len": 29,\n    "drop_columns": ["text"],\n    "disable": false,\n    "date": "2019",\n    "url": "https://en.wikipedia.org/wiki/Joke"\n    }}\n}}\n'.format(os.path.abspath(CORPUS_PATH + '-parsed'))
CORPUS = '\n<meta doc-type="joke" rating=6.50 speaker="NARRATOR"/>\n<meta being="animal">A lion</meta> and <meta being="animal">a cheetah</meta> decide to race. <meta move="setup" dialog=false punchline=false some-schema=9 />\nThe cheetah crosses the finish line first. <meta move="setup" dialog=false punchline=false />\nCHEETAH: I win! <meta move="middle" dialog=true some-schema=2 />\nLION: You\'re a <meta play-on="cheater">cheetah</meta>! <meta move="punchline" funny=true dialog=true some-schema=3 />\nCHEETAH: You\'re <meta play-on="lying">lion</meta>! <meta move="punchline" funny=true dialog=true some-schema=4 rating=7.8 />\n'
os.makedirs(FULLNAME)
for folder in ('csv', 'uploads', 'example'):
    os.makedirs(os.path.join(FULLNAME, folder))

with open(os.path.join(FULLNAME, '.env'), 'w') as (fo):
    fo.write(ENV.strip() + '\n')
with open(os.path.join(FULLNAME, 'corpora.json'), 'w') as (fo):
    fo.write(CORPORA.strip() + '\n')
with open(os.path.join(CORPUS_PATH, '001-joke-lion-pun.txt'), 'w') as (fo):
    fo.write(CORPUS.strip() + '\n')
print('Testing parser: {}->{}-parsed ...'.format(CORPUS_PATH, CORPUS_PATH))
parsed = Corpus(CORPUS_PATH).parse(cons_parser=None)
print('Workspace made in {}'.format(FULLNAME))
print("Run 'cd {} && python -m buzzword' to start.".format(NAME))