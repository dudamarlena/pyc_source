# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notepaper/paper.py
# Compiled at: 2019-12-05 09:14:51
# Size of source mod 2**32: 487 bytes
__all__ = [
 'get_paper_list']
import os

def get_paper_list():
    paper_list = [
     {'name':'DeepFM: A Factorization-Machine based Neural Network for CTR Prediction', 
      'url':'https://arxiv.org/pdf/1703.04247.pdf', 
      'year':2017},
     {'url': 'https://arxiv.org/pdf/1703.04247.pdf'}]
    return paper_list


papers = get_paper_list()
print(os.listdir('../'))
doc = open('../README.md', 'r').read()
print(doc)