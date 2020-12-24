# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pyndexter/stemmers/snowball.py
# Compiled at: 2007-02-15 02:35:50
__doc__ = "\nSnowball\n--------\n\n`Snowball <http://snowball.tartarus.org/>`_ is a multi-language stemming\nlibrary with `Python bindings <http://snowball.tartarus.org/wrappers/PyStemmer-1.0.1.tar.gz>`_.\n\nUsage\n~~~~~\n\n::\n\n    snowball://<language>\n\n``<language>``\n    Any of the languages supported by Snowball.\n\n\nInstallation\n~~~~~~~~~~~~\n\nThe Python bindings ship with the Snowball source, so it's an easy (and\nrecommended) install.\n\n::\n\n    easy_install http://snowball.tartarus.org/wrappers/PyStemmer-1.0.1.tar.gz\n\n"
import Stemmer
from pyndexter import PluginFactory

class SnowballStemmer(object):
    __module__ = __name__

    def __init__(self, language):
        self.stemmer = Stemmer.Stemmer(language)

    def __call__(self, word):
        return self.stemmer.stemWord(word)


stemmer_factory = PluginFactory(SnowballStemmer, host='language')