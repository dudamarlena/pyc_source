# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/pyramid_oauth2_provider/scripts/initializedb.py
# Compiled at: 2013-02-09 19:59:16
import os, sys
from sqlalchemy import engine_from_config
from pyramid.paster import get_appsettings, setup_logging
from ..models import DBSession, Base

def usage(argv):
    cmd = os.path.basename(argv[0])
    print 'usage: %s <config_uri>\n(example: "%s development.ini")' % (
     cmd, cmd)
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)