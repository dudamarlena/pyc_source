# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/blogs/tests/testapp/models.py
# Compiled at: 2012-02-02 00:29:51
"""
short module explanation

AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__AUTHOR__ = 'lambdalisue (lambdalisue@hashnote.net)'
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from author.decorators import with_author

@with_author
class Article(models.Model):
    PUB_STATES = (
     ('draft', 'draft'),
     ('inspecting', 'inspecting'),
     ('published', 'published'))
    pub_state = models.CharField('publish status', max_length=10, choices=PUB_STATES, default='draft')
    title = models.CharField('title', max_length=50, default='No title')
    body = models.TextField('body', blank=True, default='')
    inspectors = models.ManyToManyField(User, related_name='inspected_articles')
    group = models.ForeignKey(Group, related_name='articles', blank=True, null=True)

    def __unicode__(self):
        return self.title