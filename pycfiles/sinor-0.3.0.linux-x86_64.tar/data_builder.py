# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mahnve/.virtualenvs/blog/lib/python2.7/site-packages/test/data_builder.py
# Compiled at: 2015-04-12 05:10:26


class PostDataBuilder:

    def __init__(self):
        self.content = 'Content not set'
        self.status = ''
        self.title = 'Title not set'
        self.date = ''
        self.tags = []
        self.relative_url = ''

    def with_content(self, content=''):
        self.content = content
        return self

    def with_status(self, status):
        self.status = status
        return self

    def with_title(self, title=''):
        self.title = title
        return self

    def with_date(self, date=''):
        self.date = date
        return self

    def with_tags(self, *tags):
        self.tags = tags
        return self

    def build(self):
        return {'content': self.content, 'status': self.status, 
           'date': self.date, 
           'title': self.title, 
           'relative_url': self.relative_url, 
           'tags': self.tags}


class HTMLContentBuilder:

    def __init__(self):
        self.post_date = ''
        self.draft = ''
        self.title = ''
        self.content = ''
        self.status = ''
        self.tags = ''

    def with_post_date(self, date):
        self.post_date = ("<div id='post-date'>{}</div>").format(date)
        return self

    def with_draft_status(self):
        self.status = '<div class="draft"></div>'
        return self

    def with_title(self, title):
        self.title = ("<div id='post-title'>{}</div>").format(title)
        return self

    def with_content(self, content):
        self.content = ('<div id=post-content>{}</div>').format(content)
        return self

    def with_tags(self, *tags):
        start_tag = '<ul id="post-tags">'
        lis = reduce(lambda t: ('<li>{}</li>').format(t), tags, '')
        end_tag = '</ul>'
        self.tags = start_tag + lis + end_tag
        return self

    def build(self):
        return self.status + self.post_date + self.title + self.content