# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/ponyexpress/manage.py
# Compiled at: 2011-09-15 19:32:25
from flask import Flask
import os, couch, core
from couchdbkit.loaders import FileSystemDocsLoader
app = Flask(__name__)
app.config.from_envvar('PONYEXPRESS_CFG')

def couch_sync():
    couch_db = couch.init(app.config)
    path = os.getcwd()
    path = path.replace('/manage.py', '')
    if not path:
        return 'You must provide the path to PonyExpress'
    dir = '%s/ponyexpress/_design' % path
    print 'Syncronizing Couchdb Views from %s' % dir
    loader = FileSystemDocsLoader(dir)
    loader.sync(couch_db, verbose=True)


def queue():
    print ''
    print 'Connecting to Couchdb...'
    couch.init(app.config)
    i = 0
    for doc in couch.PonyExpressMessage.by_status(status='queued', limit=250).all():
        i += 1
        rs = {}
        try:
            pony = core.PonyExpress.from_couchdb(doc=doc)
            rs = pony.send(config=app.config)
        except Exception, e:
            print 'Exception: %s' % e

        if (rs or {}).get('result'):
            print 'Success: %s' % doc._id
        else:
            print 'Failed: %s' % doc._id

    print 'Finished processing %s messages' % i
    print ''