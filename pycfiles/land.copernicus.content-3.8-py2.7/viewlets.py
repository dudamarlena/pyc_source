# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/land/copernicus/content/browser/viewlets.py
# Compiled at: 2018-02-01 12:07:14
import os, re
from plone.app.layout.viewlets import ViewletBase

class SentryViewlet(ViewletBase):
    """Sentry script viewlet"""

    def render(self):
        return super(ViewletBase, self).render()

    def get_dsn(self):
        dsn = os.environ.get('SENTRY_DSN')
        if dsn:
            passwd = re.search('.*(:.*?)@.*', dsn).group(1)
            return dsn.replace(passwd, '')