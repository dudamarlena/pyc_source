# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/WikiTemplates/upgrades/db1.py
# Compiled at: 2007-11-10 06:34:56
import os.path, os, sys
from pkg_resources import resource_filename
from trac.core import TracError
from trac.db import DatabaseManager
from WikiTemplates.db_schema import version as templates_version, schema

def do_upgrade(env, ver, db):
    print 'Upgrading WikiTemplates plugin...'
    try:
        cursor = db.cursor()
        (db_backend, _) = DatabaseManager(env)._get_connector()
        try:
            QUERY = 'INSERT INTO system VALUES (%s,%s)'
            cursor.execute(QUERY, ('templates_version', templates_version))
            ADD_PERMS = True
        except:
            QUERY = 'UPDATE system SET value=%s WHERE name=%s'
            cursor.execute(QUERY, (templates_version, 'templates_version'))

        print ' * Creating database table...',
        try:
            for table in schema:
                for stmt in db_backend.to_sql(table):
                    env.log.debug(stmt)
                    cursor.execute(stmt)

            print ' done'
        except Exception, e:
            print ' failed'
            env.log.error(e, exc_info=1)
            db.rollback()
            raise TracError, e

        print ' * Adding default templates to database...',
        try:
            import time
            deflt_templates_dir = resource_filename('WikiTemplates', 'DefaultTemplates')
            for tpl in os.listdir(deflt_templates_dir):
                env.log.debug("Template: '%s'" % tpl)
                f = open(os.path.join(deflt_templates_dir, tpl))
                body = f.read()
                f.close()
                QUERY = 'INSERT INTO templates VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
                vals = (tpl,
                 1,
                 int(time.time()),
                 'Wiki Templates Plugin',
                 '',
                 body,
                 '',
                 0)
                cursor.execute(QUERY, vals)

            env.log.debug('First time installing Trac Wiki ' + 'Templates plugin version >= 0.3')
            print 'done'
        except Exception, e:
            print 'failed'
            env.log.debug('Failed to include default templates')
            env.log.error(e, exc_info=1)
            db.rollback()
            raise TracError, e

        print ' * Including default permissions...',
        try:
            for perm in ('VIEW', 'CREATE', 'MODIFY'):
                QUERY = 'INSERT INTO permission VALUES (%s,%s)'
                vals = ('anonymous', 'TEMPLATES_' + perm)
                cursor.execute(QUERY, vals)

            print ' done'
        except Exception, e:
            print ' failed'
            env.log.debug('Failed to include default templates permissions')
            env.log.error(e, exc_info=1)
            db.rollback()
            raise TracError, e

        print ' * Migrating old templates',
        try:
            QUERY = "SELECT * FROM wiki WHERE name LIKE '%templates/%'"
            cursor.execute(QUERY)
            rows = cursor.fetchall()
            env.log.debug('Found %d < 0.3 templates', len(rows))
            for row in rows:
                try:
                    QUERY = 'INSERT INTO templates ' + 'VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
                    VALS = (row[0].split('/').pop(1),
                     int(row[1]),
                     int(row[2]),
                     row[3],
                     row[4],
                     row[5].replace('[[Image(wiki:templates/', '[[Image(templates:'),
                     row[6],
                     int(row[7]))
                    cursor.execute(QUERY, VALS)
                    sys.stdout.write('.')
                except Exception, e:
                    print ' failed'
                    env.log.error(e, exc_info=1)
                    db.rollback()
                    raise TracError, e

            print ' done'
        except Exception, e:
            print ' No Wiki templates from versions < 0.3 found.'
            env.log.debug('No wiki templates from versions < 0.3 found.')

        print ' * Deleting old templates...',
        try:
            env.log.debug('Deleting old templates from the ' + "'templates/' sub-wiki")
            QUERY = "DELETE FROM wiki WHERE name LIKE '%templates/%'"
            env.log.debug(QUERY)
            cursor.execute(QUERY)
            print ' done'
        except Exception, e:
            print ' failed'
            env.log.debug('Failed to delete old templates from ' + "the 'templates/' sub-wiki")
            env.log.error(e, exc_info=1)
            db.rollback()
            raise TracError, e

        print ' * Migrating attachments from versions < 0.3 ...',
        try:
            query = "SELECT * FROM attachment WHERE id LIKE '%templates/%'"
            cursor.execute(query)
            rows = cursor.fetchall()
            if not rows:
                print 'No attachments found'
            else:
                try:
                    query = "SELECT * FROM attachment WHERE id LIKE '%templates/%'"
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    for row in rows:
                        col = []
                        query = 'UPDATE attachment SET type=%s, id=%s WHERE\n                        filename=%s AND size=%s AND time=%s AND description=%s AND\n                        author=%s AND ipnr=%s'
                        col.append('templates')
                        col.append(row[1].split('/').pop(1))
                        col.append(row[2])
                        col.append(row[3])
                        col.append(row[4])
                        col.append(row[5])
                        col.append(row[6])
                        col.append(row[7])
                        cursor.execute(query, col)
                        sys.stdout.write('.')

                    print ' done'
                except Exception, e:
                    print ' failed'
                    db.rollback()
                    env.log.error(e, exc_info=1)
                    raise TracError, e

                try:
                    print ' * Moving attachements to new dir',
                    from shutil import move, copytree
                    move(os.path.join(env.path, 'attachments/wiki/templates'), os.path.join(env.path, 'attachments/templates'))
                    print ' done'
                    print '  * You should confirm that the attachments have ' + 'the permissions correctly set.'
                except Exception, e:
                    print ' failed'
                    env.log.error(e, exc_info=1)
                    raise TracError, e

        except:
            pass

        db.commit()
    except Exception, e:
        db.rollback()
        env.log.error(e, exc_info=1)
        raise TracError, e