# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danjac/petprojects/tesla/tests/output/ProjectName/projectname/model/news.py
# Compiled at: 2007-09-06 07:54:25
from elixir import *

class NewsItem(Entity):
    has_field('title', String(100))
    has_field('content', String)
    using_options(tablename='newsitems')