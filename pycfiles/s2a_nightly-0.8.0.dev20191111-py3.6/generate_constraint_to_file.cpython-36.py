# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seq2annotation/helper/generate_constraint_to_file.py
# Compiled at: 2019-09-03 03:37:41
# Size of source mod 2**32: 474 bytes
import json
from seq2annotation.helper.generate_constraint import generate_constraint
from tokenizer_tools.tagset.offset.corpus import Corpus

def generate_constraint_to_file(input_file: str, output_file: str, output_attr: str='label'):
    corpus = Corpus.read_from_file(input_file)
    domain_mapping = generate_constraint(corpus, output_attr)
    with open(output_file, 'wt') as (fd):
        json.dump(domain_mapping, fd, indent=4, ensure_ascii=False)