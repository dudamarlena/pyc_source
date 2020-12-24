# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyndexter/stemmers/snowball.py
# Compiled at: 2007-02-15 02:35:50
"""
Snowball
--------

`Snowball <http://snowball.tartarus.org/>`_ is a multi-language stemming
library with `Python bindings <http://snowball.tartarus.org/wrappers/PyStemmer-1.0.1.tar.gz>`_.

Usage
~~~~~

::

    snowball://<language>

``<language>``
    Any of the languages supported by Snowball.

Installation
~~~~~~~~~~~~

The Python bindings ship with the Snowball source, so it's an easy (and
recommended) install.

::

    easy_install http://snowball.tartarus.org/wrappers/PyStemmer-1.0.1.tar.gz

"""
import Stemmer
from pyndexter import PluginFactory

class SnowballStemmer(object):
    __module__ = __name__

    def __init__(self, language):
        self.stemmer = Stemmer.Stemmer(language)

    def __call__(self, word):
        return self.stemmer.stemWord(word)


stemmer_factory = PluginFactory(SnowballStemmer, host='language')