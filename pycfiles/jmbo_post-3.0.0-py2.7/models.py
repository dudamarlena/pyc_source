# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/post/models.py
# Compiled at: 2017-07-03 11:37:50
import markdown
from bs4 import BeautifulSoup
from django.db import models
from django.core.urlresolvers import reverse
from simplemde.fields import SimpleMDEField
from jmbo.models import ModelBase

class Post(ModelBase):
    autosave_fields = ('markdown', )
    markdown = SimpleMDEField(null=True, blank=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    @property
    def content(self):
        if not self.markdown:
            return ''
        return markdown.markdown(self.markdown)

    @property
    def content_pages(self):
        marker = '--m-a-r-k-er--'
        soup = BeautifulSoup(self.content, 'html.parser')
        elems = soup.find_all('hr')
        for elem in elems:
            elem.replace_with(marker)

        return soup.renderContents().split(marker)