# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/python/post_builder.py
# Compiled at: 2016-05-16 11:23:13
# Size of source mod 2**32: 736 bytes
from main import *
import os, time

class Post:
    __doc__ = 'A post generator for Pyder, a static blog generator'

    def __init__(self, title, author):
        """Initialize attributes on a post-to-post basis. This consists of generating a dir with the date, then the name of the post."""
        self.title = title
        currentDate = str(time.strftime('%d.%m.%Y'))
        self.genDate = currentDate
        self.author = author.upper()
        os.mkdir('posts/' + self.genDate)
        fileTitle = self.title.lower()[0:15].replace(' ', '_')
        f = open('posts/' + self.genDate + fileTitle + '.md', 'w')
        content = ''
        content += str('#' + self.title + '\n\n')
        content += str('###### By ' + self.author + '\n\n')
        f.write(content)