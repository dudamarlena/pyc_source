# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seq2annotation/helper/collect_tag_to_file.py
# Compiled at: 2019-09-03 03:28:09
# Size of source mod 2**32: 249 bytes
from typing import List
from tokenizer_tools.conllz.tag_collector import collect_entity_to_file

def collect_tag_to_file(input_file_list: List[str], output_file: str):
    collect_entity_to_file(input_file_list, output_file)