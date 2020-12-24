# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonyzhao/anaconda2/lib/python2.7/site-packages/soco_core/examples.py
# Compiled at: 2020-04-17 14:36:35
import json
from soco_core.convertors import DocConvert
import os

def load_example_frame_data(name):
    cur_path = os.path.dirname(os.path.abspath(__file__))
    if name == 'mr-sun':
        doc = json.load(open(os.path.join(cur_path, '..', 'resources/mr-sun.json')))
        frames = DocConvert.document_to_frames(doc, lang='en', doc_meta={'doc_id': 'mr.sun', 'doc_title': 'Our Mr. Sun'})
        return frames
    raise Exception(('Unknown {} frame example').format(name))


def load_example_doc_data(names):
    cur_path = os.path.dirname(os.path.abspath(__file__))
    docs = []
    for n in names:
        doc = json.load(open(os.path.join(cur_path, '..', ('resources/{}').format(n))))
        docs.append(doc)

    return docs


if __name__ == '__main__':
    x = load_example_doc_data(['mr-sun.json', 'technology.json'])
    print x