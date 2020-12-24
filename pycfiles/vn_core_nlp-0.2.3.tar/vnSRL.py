# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hoang/Desktop/vn_core_nlp/vn_core_nlp/semantic_role_labeling/vnSRL.py
# Compiled at: 2016-05-17 23:09:13
from subprocess import Popen
import os
path = os.path.dirname(os.path.realpath(__file__)) + '/src/vnSRL-1.0.0'

class vnSRL(object):

    def predict(self, input_dir, output_dir, ilp, embedding):
        Popen(['python', 'vnSRL.py', input_dir, ilp, embedding, output_dir], cwd=path).communicate()