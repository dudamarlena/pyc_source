# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/apps/rating.py
# Compiled at: 2017-02-04 06:31:15
# Size of source mod 2**32: 634 bytes
import os
from analyzer.rating import Rating
from analyzer.model import Author
from analyzer.model import Article

def rating():
    user = os.environ.get('PTI_USER')
    password = os.environ.get('PTI_PASSWORD')
    host = os.environ.get('PTI_HOST')
    db = os.environ.get('PTI_DB')
    articles = Article.load_from_mysql(user, password, host, db, '/var/pti/topic')
    r = Rating(articles)
    r.calc()
    authors = Author.load_from_mysql(user, password, host, db)
    for a in authors:
        rate = r.get_author_rate(a.id)
        a.rate = rate
        a.save(user, password, host, db)


if __name__ == '__main__':
    rating()