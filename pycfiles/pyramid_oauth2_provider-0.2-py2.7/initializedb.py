# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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