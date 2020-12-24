# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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