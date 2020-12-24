# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/pyramid_oauth2_provider/scripts/create_client_credentials.py
# Compiled at: 2013-02-09 19:59:16
import os, sys, transaction
from sqlalchemy import engine_from_config
from pyramid.paster import get_appsettings, setup_logging
from pyramid_oauth2_provider.models import DBSession, initialize_sql, Oauth2Client

def create_client():
    client = Oauth2Client()
    DBSession.add(client)
    return (
     client.client_id, client.client_secret)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print 'usage: %s <config_uri> <section>\n(example: "%s development.ini myproject")' % (
     cmd, cmd)
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 3:
        usage(argv)
    config_uri = argv[1]
    section = argv[2]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, section)
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine, settings)
    with transaction.manager:
        id, secret = create_client()
        print 'client_id:', id
        print 'client_secret:', secret


if __name__ == '__main__':
    import epdb
    sys.excepthook = epdb.excepthook()
    main()