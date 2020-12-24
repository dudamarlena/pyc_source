# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./senpy/plugins/misc/split_plugin.py
# Compiled at: 2019-03-27 06:19:17
from senpy.plugins import Transformation
from senpy.models import Entry
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.tokenize.simple import LineTokenizer
import nltk

class Split(Transformation):
    """A sample plugin that chunks input text"""
    author = [
     '@militarpancho', '@balkian']
    version = '0.3'
    url = 'https://github.com/gsi-upm/senpy'
    nltk_resources = ['punkt']
    extra_params = {'delimiter': {'description': 'Split text into paragraphs or sentences.', 
                     'aliases': [
                               'type', 't'], 
                     'required': False, 
                     'default': 'sentence', 
                     'options': [
                               'sentence', 'paragraph']}}

    def analyse_entry(self, entry, activity):
        yield entry
        chunker_type = activity.params['delimiter']
        original_text = entry['nif:isString']
        if chunker_type == 'sentence':
            tokenizer = PunktSentenceTokenizer()
        if chunker_type == 'paragraph':
            tokenizer = LineTokenizer()
        chars = list(tokenizer.span_tokenize(original_text))
        if len(chars) == 1:
            return
        for i, chunk in enumerate(chars):
            start, end = chunk
            e = Entry()
            e['nif:isString'] = original_text[start:end]
            if entry.id:
                e.id = entry.id + ('#char={},{}').format(start, end)
            yield e

    test_cases = [
     {'entry': {'nif:isString': 'Hello. World.'}, 
        'params': {'delimiter': 'sentence'}, 
        'expected': [
                   {'nif:isString': 'Hello.'},
                   {'nif:isString': 'World.'}]},
     {'entry': {'@id': ':test', 
                  'nif:isString': 'Hello\nWorld'}, 
        'params': {'delimiter': 'paragraph'}, 
        'expected': [
                   {'@id': ':test#char=0,5', 
                      'nif:isString': 'Hello'},
                   {'@id': ':test#char=6,11', 
                      'nif:isString': 'World'}]}]