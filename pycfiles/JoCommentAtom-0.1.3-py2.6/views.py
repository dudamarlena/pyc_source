# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/jocommentatom/views.py
# Compiled at: 2010-12-27 16:35:37
from pyramid.httpexceptions import HTTPMovedPermanently
from sqlalchemy import desc
from jocommentatom.models import DBSession, Comment

def atom_feed(request):
    """Generate atom feed."""
    settings = request.registry.settings
    dbsession = DBSession()
    comments = dbsession.query(Comment).order_by(desc(Comment.date))
    latest_comments = comments.limit(settings.limit).all()
    site_url = settings.get('site_url')
    title = settings.get('title')
    subtitle = settings.get('subtitle')
    author_name = settings.get('author.name')
    author_email = settings.get('author.email')
    updated = comments[0].rfc3339date
    return {'site_url': site_url, 'title': title, 'subtitle': subtitle, 'author_name': author_name, 
       'author_email': author_email, 'updated': updated, 
       'comments': latest_comments}


def notfound_view(request):
    """Not found.

    Redirect to /
    """
    return HTTPMovedPermanently(location=request.route_url('home'))