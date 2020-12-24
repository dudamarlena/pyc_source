# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/weakpoint/slides.py
# Compiled at: 2012-11-21 04:46:57
import re

class Slide(object):

    def __init__(self, **arg):
        self.no = arg['no']
        self.content = arg['content']
        self.chapter = arg['chapter']
        self.section = arg['section']


class Navi(object):

    def __init__(self, **arg):
        self.title = arg['title']
        self.no = arg['no']


class Slides(object):
    """
    The slides no begins from 2!!!
    """

    def __init__(self, content):
        slides = re.compile('<hr>').split(content)
        self.slides = []
        self.navi = []
        chapter = -1
        section = -1
        for i in range(len(slides)):
            section += 1
            content = slides[i]
            titles = re.compile('<h1>.*?<\\/h1>').findall(content)
            if titles:
                chapter += 1
                section = 0
                titlestring = titles[0].replace('<h1>', '')
                titlestring = titlestring.replace('</h1>', '')
                self.navi.append(Navi(title=titlestring, no=i + 2))
            self.slides.append(Slide(no=i + 2, content=content, section=section, chapter=chapter))