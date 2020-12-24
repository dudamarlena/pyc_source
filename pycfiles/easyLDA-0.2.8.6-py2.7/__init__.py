# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/easyLDA/__init__.py
# Compiled at: 2018-02-04 10:53:57
import nltk
print 'downloading nltk data'
nltk.download('stopwords')
nltk.download('wordnet')
from .base import PipelineLDA
from .base import main as LDA_main

def main():
    print 'executing...'
    LDA_main()