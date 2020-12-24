# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: backstage/db/db_utils.py
# Compiled at: 2014-07-08 11:32:40
__author__ = 'walker'
import os, psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from django.conf import settings
from django.core.management import call_command

def get_dsn(inst):
    """ build the psycopg2 connection dsn
    @param inst:
    @return:
    """
    try:
        if inst.dsn is not None and inst.dsn_backstage is not None:
            return (inst.dsn, inst.dsn_backstage)
    except:
        pass

    db = get_default_db(inst)
    dsn = 'dbname=%s port=%s host=%s' % (db['NAME'], db['PORT'], db['HOST'])
    dsn_backstage = 'dbname=backstage port=%s host=%s' % (db['PORT'], db['HOST'])
    inst.dsn = dsn
    inst.dsn_backstage = dsn_backstage
    return (dsn, dsn_backstage)


def get_default_db(inst):
    """
    return the instance's default db
    @param inst:
    @return:
    """
    try:
        db = inst.settings.DATABASES['default']
        return db
    except:
        print 'error getting database'
        return

    return


def connect_default(inst):
    """
    Connect this instance to its default database, as defined in settings
    @param inst: Backstage Act or Venue instance
    @return:
    """
    try:
        dsn, dsn_backstage = get_dsn(inst)
        conn = psycopg2.connect(dsn)
        inst.conn = conn
        return conn
    except psycopg2.OperationalError as e:
        if 'does not exist' in str(e):
            s = str(e).replace('FATAL:', '').strip()
            s += '\nHint: try "backstage.db.db_utils.create_default()"'
            print s
            return
        else:
            print e
            return

    return


def sync_default(inst):
    """
    Sync the default database
    @param inst:
    @return:
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.settings' % inst.name)
    os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % inst.name
    call_command('syncdb', verbosity=0, interactive=False, settings='%s.settings' % inst.name)


def migrate_default(inst):
    """
    Migrate the default database
    @param inst:
    @return:
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.settings' % inst.name)
    os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % inst.name
    call_command('migrate', interactive=False, verbosity=0, settings='%s.settings' % inst.name)


def create_default(inst):
    """
    Create a backstage database for a given backstage instance
    @param inst:
    @return:
    """
    try:
        dsn, dsn_backstage = get_dsn(inst)
    except Exception as e:
        print 'Error getting the dsn info'
        print e
        raise

    try:
        conn = psycopg2.connect(dsn)
        if isinstance(conn, psycopg2._psycopg.connection):
            print 'Database already exists'
            return
    except:
        pass

    try:
        conn = psycopg2.connect(dsn_backstage)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        db = get_default_db(inst)
        dbname = db['NAME']
        q = 'CREATE DATABASE %s' % dbname
        cur.execute(q)
        conn.commit()
        cur.close()
        conn.close()
        print 'Successfully created Act database %s' % dbname
        return
    except Exception as e:
        print e
        raise