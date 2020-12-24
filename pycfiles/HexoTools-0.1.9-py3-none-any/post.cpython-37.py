# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\projects\hexotools\hexotools\postprocess\post.py
# Compiled at: 2019-10-12 03:41:53
# Size of source mod 2**32: 4069 bytes
import os, re
from zlib import crc32

class Post:

    def __init__(self, title='', cate='', tags=[], date='', updated='', abbrlink=''):
        self.title = title
        self.cate = cate
        self.tags = tags
        self.abbrlink = abbrlink
        self.date = date
        self.updated = updated

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, tags):
        self._tags = tags

    @property
    def cate(self):
        return self._cate

    @cate.setter
    def cate(self, cate):
        self._cate = cate

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    @property
    def updated(self):
        return self._updated

    @updated.setter
    def updated(self, updated):
        self._updated = updated

    @property
    def abbrlink(self):
        return self._abbrlink

    @abbrlink.setter
    def abbrlink(self, abbrlink):
        self._abbrlink = abbrlink


class EditCate:

    def __init__(self):
        pass

    @staticmethod
    def getMDFlie(folder):
        for root, dirs, files in os.walk(folder):
            for i in files:
                if os.path.splitext(i)[(-1)] == '.md':
                    i = os.path.join(root, i)
                    yield i

    @staticmethod
    def getWriteContent(file_path, root):
        file_path = os.path.relpath(file_path, root).split(os.path.sep)[:-1]
        i = 0
        content = []
        while file_path:
            content.append('  - ' + file_path.pop() + '\n')

        return content

    @staticmethod
    def writeToFile(file_path, content):
        with open(file_path, 'r', encoding='utf-8') as (fo):
            text = fo.readlines()
            i = 0
            if not text:
                return
            while True:
                if re.match('categories:.*', text[i]):
                    while True:
                        if re.match('(.*:.*)|(---)', text[(i + 1)]):
                            break
                        else:
                            del text[i + 1]

                    while content:
                        text.insert(i + 1, content.pop())

                    break
                else:
                    i += 1

        with open(file_path, 'w', encoding='utf-8') as (fo):
            fo.writelines(text)


class NewPost(Post):

    def getPath(self, posts_path):
        r = (os.path.join)(os.path.normpath(posts_path), *self.cate, *(
         '%s.md' % self.title,))
        return (os.path.join)(os.path.normpath(posts_path), *self.cate, *(
         '%s.md' % self.title,))

    def getWriteContent(self):
        yield '---\n'
        yield 'title: %s\n' % self.title
        yield 'date: %s\n' % self.date
        yield 'categories:\n'
        for i in range(len(self.cate)):
            yield '  - %s\n' % self.cate[i]

        yield 'tags:\n'
        for i in range(len(self.tags)):
            yield '  - %s\n' % self.tags[i]

        yield 'updated:\n'

    def newPost(self, posts_path):
        path = self.getPath(posts_path)
        os.makedirs((os.path.dirname(path)), exist_ok=True)
        with open(path, 'a+', encoding='utf-8') as (fo):
            fo.writelines(self.getWriteContent())
            fo.seek(0, 0)
            self.abbrlink = hex(crc32(fo.read().encode('utf-8')))[2:]
            fo.write('abbrlink: %s\n' % self.abbrlink)
            fo.write('---\n')