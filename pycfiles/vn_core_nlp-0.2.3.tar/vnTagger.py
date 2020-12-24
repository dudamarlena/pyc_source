# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hoang/Desktop/vn_core_nlp/vn_core_nlp/preprocessing/pos_tagger/vnTagger.py
# Compiled at: 2016-05-17 23:05:33
from subprocess import Popen
import os
path = os.path.dirname(os.path.realpath(__file__)) + '/src/vn.hus.nlp.tagger-4.2.0-bin'

class vnTagger(object):

    def pos_tagger(self, input_dir, output_dir, output_type='', underscore=''):
        Popen(['./vnTagger.sh', '-i', input_dir, '-o', output_dir, output_type, underscore], cwd=path).communicate()