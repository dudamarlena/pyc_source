# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seq2annotation/preprocess_hooks/corpus_drop.py
# Compiled at: 2019-10-16 22:50:53
# Size of source mod 2**32: 1276 bytes
import copy
from seq2annotation.preprocess_hooks.hook_base import HookBase
from tokenizer_tools.tagset.offset.sequence import Sequence
from tokenizer_tools.tagset.offset.span import Span

class CorpusAugment(HookBase):
    punctuation = [
     '。',
     '.',
     '？',
     '?',
     '！',
     '!']

    def __call__(self, sentence):
        text = sentence.text
        text_str = ''.join(text)
        no_tail_text = text_str.rstrip(''.join(self.punctuation))
        result = []
        for i in self.punctuation:
            new_sentence = copy.deepcopy(sentence)
            new_sentence.text = [i for i in ''.join((no_tail_text, i))]
            result.append(new_sentence)

        new_sentence = copy.deepcopy(sentence)
        new_sentence.text = [i for i in no_tail_text]
        result.append(new_sentence)
        return result[(-1)]


if __name__ == '__main__':
    seq = Sequence('王小明在北京的清华大学读书。')
    seq.span_set.append(Span(0, 3, 'PERSON', '王小明'))
    seq.span_set.append(Span(4, 6, 'GPE', '北京'))
    seq.span_set.append(Span(7, 11, 'ORG', '清华大学'))
    ca = CorpusAugment()
    res = ca(seq)
    print(res)