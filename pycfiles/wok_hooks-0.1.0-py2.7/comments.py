# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wok_hooks/comments.py
# Compiled at: 2014-10-05 10:57:35
import logging

class Post(object):

    def __init__(self, slug, title, reference, time, author, author_email, content):
        self.slug = slug
        self.title = title
        self.reference = reference
        self.author = author
        self.author_email = author_email
        self.time = time
        self.content = content

    def save(self, content_dir):
        with open('%s%s.md' % (content_dir, self.slug), 'w+') as (fd):

            def writeline(text):
                try:
                    fd.write(text.encode('utf8') + '\n')
                except Exception as ex:
                    logging.error(ex)

            writeline('title: %s' % self.title)
            writeline('slug: %s' % self.slug)
            writeline('category: %s' % self.reference)
            writeline('type: comment')
            writeline('datetime: %s' % self.time.isoformat(' '))
            writeline('author: %s' % self.author)
            writeline('author_email: %s' % self.author_email)
            writeline('---')
            writeline(self.content)