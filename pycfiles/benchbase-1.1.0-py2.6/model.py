# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/benchbase/model.py
# Compiled at: 2011-09-20 04:16:10
import os, sqlite3, logging
from sqlitext import add_aggregates
SCHEMAS = {'bench': {'md5sum': 'TEXT', 
             'filename': 'TEXT', 
             'date': 'TEXT', 
             'comment': 'TEXT', 
             'generator': 'TEXT'}, 
   'host': {'bid': 'INTEGER', 
            'host': 'TEXT', 
            'comment': 'TEXT'}, 
   'cpu': {'bid': 'INTEGER', 
           'host': 'TEXT', 
           'date': 'TEXT', 
           'usr': 'REAL', 
           'nice': 'REAL', 
           'sys': 'REAL', 
           'iowait': 'REAL', 
           'steal': 'REAL', 
           'irq': 'REAL', 
           'soft': 'REAL', 
           'guest': 'REAL', 
           'idle': 'REAL'}, 
   'disk': {'bid': 'INTEGER', 
            'host': 'TEXT', 
            'date': 'TEXT', 
            'dev': 'TEST', 
            'tps': 'REAL', 
            'rd_sec_per_s': 'REAL', 
            'wr_sec_per_s': 'REAL', 
            'util': 'REAL'}, 
   'j_testresults': {'bid': 'INTEGER', 
                     'version': 'TEXT'}, 
   'j_sample': {'bid': 'INTEGER', 
                'stamp': 'INTEGER', 
                'success': 'INTEGER', 
                'by': 'INTEGER', 
                'de': 'TEXT', 
                'dt': 'TEXT', 
                'ec': 'INTEGER', 
                'hn': 'TEXT', 
                'it': 'INTEGER', 
                'lb': 'TEXT', 
                'lt': 'INTEGER', 
                'na': 'INTEGER', 
                'ng': 'INTEGER', 
                'rc': 'INTEGER', 
                'rm': 'TEXT', 
                's': 'TEXT', 
                'sc': 'INTEGER', 
                't': 'INTEGER', 
                'tn': 'TEXT', 
                'ts': 'INTEGER', 
                'varname': 'TEXT'}, 
   'f_config': {'bid': 'INTEGER', 
                'key': 'TEXT', 
                'value': 'TEXT'}, 
   'f_response': {'bid': 'INTEGER', 
                  'stamp': 'INTEGER', 
                  'success': 'INTEGER', 
                  'lb': 'TEXT', 
                  'cycle': 'INTEGER', 
                  'cvus': 'INTEGER', 
                  'thread': 'INTEGER', 
                  'suite': 'TEXT', 
                  'name': 'TEXT', 
                  'step': 'INTEGER', 
                  'number': 'INTEGER', 
                  'type': 'TEXT', 
                  'result': 'TEXT', 
                  'url': 'TEXT', 
                  'code': 'INTEGER', 
                  'description': 'TEXT', 
                  'time': 'REAL', 
                  'duration': 'REAL'}, 
   'f_testresult': {'bid': 'INTEGER', 
                    'cycle': 'INTEGER', 
                    'cvus': 'INTEGER', 
                    'thread': 'INTEGER', 
                    'suite': 'TEXT', 
                    'name': 'TEXT', 
                    'time': 'REAL', 
                    'result': 'TEXT', 
                    'steps': 'INTEGER', 
                    'duration': 'REAL', 
                    'connection_duration': 'REAL', 
                    'requests': 'INTEGER', 
                    'pages': 'INTEGER', 
                    'xmlrpc': 'INTEGER', 
                    'redirects': 'INTEGER', 
                    'images': 'INTEGER', 
                    'links': 'INTEGER'}}
CREATE_QUERY = 'CREATE TABLE IF NOT EXISTS [{table}]({fields})'
INSERT_QUERY = 'INSERT INTO {table} ({columns}) VALUES ({values})'

def open_db(options, create=True):
    if options.rmdatabase and os.path.exists(options.database):
        logging.warning('Erasing database: ' + options.database)
        os.unlink(options.database)
        create = True
    db = sqlite3.connect(options.database)
    add_aggregates(db)
    if create:
        initialize_db(db)
    return db


def initialize_db(db):
    table_names = SCHEMAS.keys()
    for table_name in table_names:
        sql_create = CREATE_QUERY.format(table=table_name, fields=(', ').join([ ('{0} {1}').format(name, type) for (name, type) in SCHEMAS[table_name].items() ]))
        logging.debug(('Creating table {0}').format(table_name))
        try:
            logging.debug(sql_create)
            db.execute(sql_create)
        except Exception, e:
            logging.warning(e)

    db.execute('create index if not exists j_stamp_idx on j_sample (stamp)')
    db.execute('create index if not exists f_response_idx on f_response (stamp)')
    db.commit()
    return db


def list_benchmarks(db):
    c = db.cursor()
    c.execute('SELECT ROWID, date, generator, filename, comment FROM bench')
    print '%5s %-19s %-8s %-30s %s' % ('bid', 'Imported', 'Tool', 'Filename', 'Comment')
    for row in c:
        print '%5d %19s %-8s %-30s %s' % (row[0], row[1][:19], row[2], os.path.basename(row[3]), row[4])

    c.close()