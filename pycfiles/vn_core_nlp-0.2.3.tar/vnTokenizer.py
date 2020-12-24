# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hoang/Desktop/vn_core_nlp/vn_core_nlp/preprocessing/word_tokenizer/vnTokenizer.py
# Compiled at: 2016-05-17 22:50:54
from subprocess import Popen
import os
path = os.path.dirname(os.path.realpath(__file__)) + '/src/vn.hus.nlp.tokenizer-4.1.1-bin'

class vnTokenizer(object):

    def tokenize_file(self, input_dir, output_dir, output_type='', underscore='', sd=''):
        Popen(['./vnTokenizer.sh', '-i', input_dir, '-o', output_dir, output_type, underscore, sd], cwd=path).communicate()

    def tokenize_directory(self, input_dir, output_dir, output_type='', underscore='', sd='', extension=''):
        Popen(['./vnTokenizer.sh', '-i', input_dir, '-o', output_dir, output_type, underscore, sd, extension], cwd=path).communicate()