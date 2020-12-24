# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/drqa/tokenizers/corenlp_tokenizer.py
# Compiled at: 2019-08-29 06:03:42
# Size of source mod 2**32: 4550 bytes
"""Simple wrapper around the Stanford CoreNLP pipeline.

Serves commands to a java subprocess running the jar. Requires java 8.
"""
import copy, json, pexpect
from .tokenizer import Tokens, Tokenizer
from . import DEFAULTS

class CoreNLPTokenizer(Tokenizer):

    def __init__(self, **kwargs):
        """
        Args:
            annotators: set that can include pos, lemma, and ner.
            classpath: Path to the corenlp directory of jars
            mem: Java heap memory
        """
        self.classpath = kwargs.get('classpath') or DEFAULTS['corenlp_classpath']
        self.annotators = copy.deepcopy(kwargs.get('annotators', set()))
        self.mem = kwargs.get('mem', '2g')
        self._launch()

    def _launch(self):
        """Start the CoreNLP jar with pexpect."""
        annotators = [
         'tokenize', 'ssplit']
        if 'ner' in self.annotators:
            annotators.extend(['pos', 'lemma', 'ner'])
        else:
            if 'lemma' in self.annotators:
                annotators.extend(['pos', 'lemma'])
            else:
                if 'pos' in self.annotators:
                    annotators.extend(['pos'])
        annotators = ','.join(annotators)
        options = ','.join(['untokenizable=noneDelete',
         'invertible=true'])
        cmd = ['java', '-mx' + self.mem, '-cp', '"%s"' % self.classpath,
         'edu.stanford.nlp.pipeline.StanfordCoreNLP', '-annotators',
         annotators, '-tokenize.options', options,
         '-outputFormat', 'json', '-prettyPrint', 'false']
        self.corenlp = pexpect.spawn('/bin/bash', maxread=100000, timeout=60)
        self.corenlp.setecho(False)
        self.corenlp.sendline('stty -icanon')
        self.corenlp.sendline(' '.join(cmd))
        self.corenlp.delaybeforesend = 0
        self.corenlp.delayafterread = 0
        self.corenlp.expect_exact('NLP>', searchwindowsize=100)

    @staticmethod
    def _convert(token):
        if token == '-LRB-':
            return '('
        else:
            if token == '-RRB-':
                return ')'
            else:
                if token == '-LSB-':
                    return '['
                else:
                    if token == '-RSB-':
                        return ']'
                    if token == '-LCB-':
                        return '{'
                if token == '-RCB-':
                    return '}'
            return token

    def tokenize(self, text):
        if 'NLP>' in text:
            raise RuntimeError('Bad token (NLP>) in text!')
        if text.lower().strip() == 'q':
            token = text.strip()
            index = text.index(token)
            data = [(token, text[index:], (index, index + 1), 'NN', 'q', 'O')]
            return Tokens(data, self.annotators)
        else:
            clean_text = text.replace('\n', ' ')
            self.corenlp.sendline(clean_text.encode('utf-8'))
            self.corenlp.expect_exact('NLP>', searchwindowsize=100)
            output = self.corenlp.before
            start = output.find(b'{"sentences":')
            output = json.loads(output[start:].decode('utf-8'))
            data = []
            tokens = [t for s in output['sentences'] for t in s['tokens']]
            for i in range(len(tokens)):
                start_ws = tokens[i]['characterOffsetBegin']
                if i + 1 < len(tokens):
                    end_ws = tokens[(i + 1)]['characterOffsetBegin']
                else:
                    end_ws = tokens[i]['characterOffsetEnd']
                data.append((
                 self._convert(tokens[i]['word']),
                 text[start_ws:end_ws],
                 (
                  tokens[i]['characterOffsetBegin'],
                  tokens[i]['characterOffsetEnd']),
                 tokens[i].get('pos', None),
                 tokens[i].get('lemma', None),
                 tokens[i].get('ner', None)))

            return Tokens(data, self.annotators)

    def shutdown(self):
        self.corenlp.close(force=True)