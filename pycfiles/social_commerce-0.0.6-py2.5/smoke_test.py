# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialcommerce/tests/smoke_test.py
# Compiled at: 2009-10-31 23:19:40


def run():
    from django.test.client import Client
    c = Client()
    pages = [
     '/',
     '/about/',
     '/profiles/',
     '/blog/',
     '/invitations/',
     '/notices/',
     '/messages/',
     '/announcements/',
     '/tweets/',
     '/tribes/',
     '/robots.txt',
     '/photos/',
     '/bookmarks/']
    for page in pages:
        print page,
        try:
            x = c.get(page)
            if x.status_code in (301, 302):
                print x.status_code, '=>', x['Location']
            else:
                print x.status_code
        except Exception, e:
            print e