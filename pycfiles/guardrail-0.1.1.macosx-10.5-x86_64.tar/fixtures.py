# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jmcarp/miniconda/envs/guardian/lib/python2.7/site-packages/examples/flask_sqla/fixtures.py
# Compiled at: 2015-04-03 18:03:16
import models, permissions

def ensure(app):
    with app.app_context():
        user = models.db.session.query(models.User).get(1)
        if not user:
            user = models.User(id=1, username='freddie')
            models.db.session.add(user)
            models.db.session.commit()
        post = models.db.session.query(models.Post).get(1)
        if not post:
            post = models.Post(id=1, title='death on two legs', content='dedicated to...')
            models.db.session.add(post)
            models.db.session.commit()
        try:
            permissions.manager.ensure_permission(user, post, 'read')
        except:
            pass

        models.db.session.commit()