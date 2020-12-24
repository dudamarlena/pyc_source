# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/punsy/cmu.py
# Compiled at: 2020-04-04 09:06:49
# Size of source mod 2**32: 3185 bytes
import os, sys
from argparse import ArgumentParser
from pkg_resources import resource_string
import json, logging
from punsy.structs.suffix_trie import SuffixTrie
DICTIONARY_FPATH = 'data/cmudict-0.7b.utf8'

class CMU:

    def __init__(self, cmu_fpath):
        self.fpath = cmu_fpath
        self.phonemes = SuffixTrie()
        self.mapping = {}
        self.n_lines = CMU.count_lines(self.fpath)

    def run(self):
        logging.debug(f"Parsing & loading {self.n_lines} entries from CMU dictionary file")
        for word, phonemes in CMU.parse(self.fpath):
            phonemes = phonemes.split(' ')
            self.phonemes.insert(phonemes, word)
            self.mapping[word] = phonemes

    def rhymes_for(self, suffix, offset=3, max_depth=10):
        pron = self.mapping[suffix]
        logging.debug(f"""Pronunciation of "{suffix}" is "{'-'.join(pron)}"""")
        logging.debug(f"""Fetching rhymes, applying offset={offset}: "{'-'.join(pron[offset:])}"""")
        rhymes = self.phonemes.rhymes_for_suffix(pron,
          offset=offset,
          max_depth=10)
        logging.debug(f"Rhymes for {suffix}: {rhymes}")
        return rhymes

    @staticmethod
    def parse(fpath='', delimiter='|'):
        for line in CMU._CMU__iter_file(fpath):
            yield line.strip().split(delimiter)

    @staticmethod
    def count_lines(fpath=''):
        for i, _ in enumerate(CMU._CMU__iter_file(fpath)):
            pass

        return i

    @staticmethod
    def __iter_file--- This code section failed: ---

 L.  53         0  LOAD_FAST                'fpath'
                2  POP_JUMP_IF_FALSE    38  'to 38'

 L.  54         4  LOAD_GLOBAL              open
                6  LOAD_FAST                'fpath'
                8  LOAD_STR                 'r'
               10  CALL_FUNCTION_2       2  ''
               12  SETUP_WITH           30  'to 30'
               14  STORE_FAST               'istream'

 L.  55        16  LOAD_FAST                'istream'
               18  GET_YIELD_FROM_ITER
               20  LOAD_CONST               None
               22  YIELD_FROM       
               24  POP_TOP          
               26  POP_BLOCK        
               28  BEGIN_FINALLY    
             30_0  COME_FROM_WITH       12  '12'
               30  WITH_CLEANUP_START
               32  WITH_CLEANUP_FINISH
               34  END_FINALLY      
               36  JUMP_FORWARD         74  'to 74'
             38_0  COME_FROM             2  '2'

 L.  57        38  LOAD_GLOBAL              resource_string
               40  LOAD_STR                 'punsy'
               42  LOAD_GLOBAL              DICTIONARY_FPATH
               44  CALL_FUNCTION_2       2  ''
               46  LOAD_METHOD              decode
               48  CALL_METHOD_0         0  ''
               50  LOAD_METHOD              split
               52  LOAD_STR                 '\n'
               54  CALL_METHOD_1         1  ''
               56  GET_ITER         
             58_0  COME_FROM            64  '64'
               58  FOR_ITER             74  'to 74'
               60  STORE_FAST               'line'

 L.  58        62  LOAD_FAST                'line'
               64  POP_JUMP_IF_FALSE    58  'to 58'

 L.  59        66  LOAD_FAST                'line'
               68  YIELD_VALUE      
               70  POP_TOP          
               72  JUMP_BACK            58  'to 58'
             74_0  COME_FROM            36  '36'

Parse error at or near `BEGIN_FINALLY' instruction at offset 28


class POC:

    def __init__(self, cmu_fpath):
        self.cmu = CMU(cmu_fpath)
        self.cmu.run()

    def run(self, sentence, offset=1, max_depth=10):
        import random
        parts = sentence.split(' ')
        word = parts[(-1)].upper()
        rhyme = random.choice(self.cmu.rhymes_for(word,
          offset=offset, max_depth=max_depth))
        parts[-1] = rhyme
        return ' '.join(parts)


def poc():
    parser = ArgumentParser(prog='punsy')
    parser.add_argument('--sentence', type=str, required=True, help='The sentence to punnify')
    parser.add_argument('--cmu-file', type=str, help='(optional) the path of the cmu rhyming dictionary')
    parser.add_argument('--offset', type=int, default=2, help='The number of syllables to match')
    parser.add_argument('--max-depth', type=int, default=10, help='The maximum length of a matched rhyming word')
    parser.add_argument('-v', '--verbose', action='store_true', default=False)
    args = parser.parse_args()
    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(level=level, format='- %(message)s')
    result = POC(args.cmu_file).run(sentence=(args.sentence),
      offset=(args.offset))
    logging.info(f'Generated pun: "{args.sentence}" => "{result}"')


if __name__ == '__main__':
    poc()