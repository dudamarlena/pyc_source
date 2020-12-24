# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/senex/scripts/initializedb.py
# Compiled at: 2016-04-28 15:25:39
import os, sys, transaction
from sqlalchemy import engine_from_config
from pyramid.paster import get_appsettings, setup_logging
from ..models import DBSession, OLD, SenexState, Base

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
    with transaction.manager:
        senex_state = SenexState()
        DBSession.add(senex_state)