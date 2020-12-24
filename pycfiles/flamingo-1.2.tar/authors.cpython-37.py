# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/plugins/authors/authors.py
# Compiled at: 2020-03-20 06:56:10
# Size of source mod 2**32: 955 bytes
import os
from flamingo.core.utils.string import split, slugify

class Authors:
    THEME_PATHS = [
     os.path.join(os.path.dirname(__file__), 'theme')]

    def contents_parsed(self, context):
        content_key = getattr(context.settings, 'I18N_CONTENT_KEY', 'id')
        for content in context.contents:
            if content['authors']:
                content['authors'] = split(content['authors'])
            else:
                content['authors'] = []

        authors = sorted(list(set(sum(context.contents.values('authors'), []))))
        for author in authors:
            output = os.path.join('authors/{}.html'.format(slugify(author)))
            (context.contents.add)(**{content_key: '_author/{}'.format(author), 
             'output': output, 
             'url': '/' + output, 
             'author': author, 
             'template': 'author.html'})