# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidam/git/damenltk/source/test/test_detectlanguage.py
# Compiled at: 2019-10-30 01:06:48
# Size of source mod 2**32: 1347 bytes
import unittest, nltk
from nltk.corpus import stopwords
from app.detectlanguage import DetectLanguage

class TddInPythonExample(unittest.TestCase):

    def test_detectlanguage_spanish_method_returns_correct_result(self):
        dl = DetectLanguage()
        textes = '\n        En un lugar de la Mancha de cuyo nombre no quiero acordarme, vivía un ingenioso hidalgo\n        '
        self.assertEqual(dl.detect_language(textes), 'spanish')