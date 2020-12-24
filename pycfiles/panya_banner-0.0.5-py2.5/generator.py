# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/banner/generator.py
# Compiled at: 2010-12-14 06:48:44
import random
from generate import IMAGES
from generate.json_loader import load_json
BANNER_COUNT = 10

def generate():
    objects = []
    for i in range(1, BANNER_COUNT + 1):
        objects.append({'model': 'banner.ImageBanner', 
           'fields': {'title': 'Image Banner %s Title' % i, 
                      'state': 'published', 
                      'image': random.sample(IMAGES, 1)[0], 
                      'url': 'http://www.google.com', 
                      'sites': {'model': 'sites.Site', 
                                'fields': {'name': 'example.com'}}}})

    for i in range(1, BANNER_COUNT + 1):
        objects.append({'model': 'banner.CodeBanner', 
           'fields': {'title': 'Code Banner %s Title' % i, 
                      'state': 'published', 
                      'image': random.sample(IMAGES, 1)[0], 
                      'code': '<strong>strong tag</strong>', 
                      'sites': {'model': 'sites.Site', 
                                'fields': {'name': 'example.com'}}}})

    load_json(objects)