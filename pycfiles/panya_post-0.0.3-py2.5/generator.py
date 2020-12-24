# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/post/generator.py
# Compiled at: 2010-08-11 09:10:12
import random
from generate import IMAGES
from generate.json_loader import load_json
POST_COUNT = 20

def generate():
    objects = []
    for i in range(1, POST_COUNT + 1):
        objects.append({'model': 'post.Post', 
           'fields': {'title': 'Post %s Title' % i, 
                      'description': 'Post %s description with some added text to verify truncates where needed.' % i, 
                      'state': 'published', 
                      'image': random.sample(IMAGES, 1)[0], 
                      'content': '<strong>strong</strong><i>italic</i>', 
                      'sites': {'model': 'sites.Site', 
                                'fields': {'name': 'example.com'}}}})

    load_json(objects)