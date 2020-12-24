# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openspeechcorpus_cli/cmu_sphinx/generate_fileids.py
# Compiled at: 2020-01-11 08:44:43
# Size of source mod 2**32: 563 bytes
__author__ = 'ma0'
import os, codecs
unconvert_file_ids = 'ops_T22/ops_T22_etc/all.fileids'
so_path_separator = '/'
output_file = 'ops_T22/ops_T22_etc/ops_T22.fileids'
f = codecs.open(unconvert_file_ids, 'rb', encoding='UTF-8')
f_content = f.readlines()
fo = codecs.open(output_file, 'w+', encoding='UTF-8')
for line in f_content:
    if '3gp' in line:
        fo.write(line.replace('.3gp', '_3gp'))

fo.close()