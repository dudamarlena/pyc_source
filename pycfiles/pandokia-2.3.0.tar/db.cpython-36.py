# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jhunk/Downloads/pandokia/pandokia/db.py
# Compiled at: 2018-05-14 14:25:23
# Size of source mod 2**32: 11796 bytes
import sys, re, pandokia.text_table as text_table
re_funky_chars = re.compile('[^ -~]')
re_star_x_star = re.compile('^\\*[^*]*\\*$')

class name_sequence(object):

    def __init__(self):
        self.counter = 0
        self.dict = {}

    def next(self, v):
        n = str(self.counter)
        self.counter += 1
        self.dict[n] = v
        return n


class where_dict_base(object):
    __doc__ = '\n    where_dict is a mechanism for constructing SQL WHERE clauses in a\n    portable way, but without going so far from SQL as an ORM\n\n    This class exists so you can subclass from it in the database driver.\n    It is (so far) the same for every database driver.\n    '

    def where_dict(self, lst, more_where=None):
        """
            where_text, where_dict = pdk_db.where_dict( [
                ('field', value),
                ('anotherfield', anothervalue),
                ], more_where )

            c = pdk_db.execute( "SELECT col FROM tbl %s " % where_text, where_dict)
        """
        if isinstance(lst, dict):
            nl = []
            for x in lst:
                nl.append((x, lst[x]))

            lst = nl
        else:
            ns = name_sequence()
            and_list = []
            for name, value in lst:
                if value == '*' or value == '%' or value is None:
                    or_list = []
                else:
                    if not isinstance(value, list):
                        if value.startswith('[') or value.endswith(']'):
                            value = [x for x in value if x.isalnum()]
                        else:
                            value = [
                             value]
                    or_list = []
                    for v in value:
                        if v is None or v == '*' or v == '%':
                            or_list = []
                            break
                        v = str(v)
                        v = re_funky_chars.sub('', v)
                        if '%' in v:
                            n = ns.next(v)
                            or_list.append(' %s LIKE :%s ' % (name, n))
                        elif '*' in v:
                            if v.startswith('*'):
                                v = '%' + v[1:]
                            elif v.endswith('*'):
                                v = v[:-1] + '%'
                            elif '*' in v:
                                assert 0, 'GLOB not supported except *xx or xx* '
                            n = ns.next(v)
                            or_list.append(' %s LIKE :%s ' % (name, n))
                        elif '*' in v or '?' in v or '[' in v:
                            print('content-type: text/plain\n')
                            print(lst)
                            print(v)
                            return
                        else:
                            n = ns.next(v)
                            or_list.append(' %s = :%s ' % (name, n))

                if len(or_list) > 0:
                    and_list.append(' ( %s ) ' % ' OR '.join(or_list))

            res = ' AND '.join(and_list)
            if more_where:
                if res != '':
                    res = ' %s AND %s ' % (res, more_where)
                else:
                    res = more_where
            if res != '':
                res = 'WHERE ' + res
        return (
         res, ns.dict)

    def table_to_csv(self, tablename, fname, where='', cols=None):
        if cols is None:
            c = self.execute('SELECT * FROM %s LIMIT 1' % tablename)
            cols = [x[0] for x in c.description]
            c.close()
        else:
            colstr = ','.join(cols)
            import csv
            if isinstance(fname, str):
                f = open(fname, 'wb')
            else:
                f = fname
        cc = csv.writer(f, lineterminator='\n')
        cc.writerow(cols)
        print(colstr)
        print('ORDER %s' % colstr)
        c = self.execute('select %s from %s %s order by %s' % (
         colstr, tablename, where, colstr))
        for x in c:
            cc.writerow([y for y in x])

        c.close()
        if not isinstance(fname, str):
            f.close()

    def query_to_csv(self, query, fname):
        import csv
        if isinstance(fname, str):
            f = open(fname, 'wb')
        else:
            f = fname
        cc = csv.writer(f, lineterminator='\n')
        c = self.execute(query)
        for x in c:
            cc.writerow([y for y in x])

        c.close()
        if not isinstance(fname, str):
            f.close()

    def sql_commands(self, s, format='rst'):
        s = s.split('\n')
        import re
        comment = re.compile('--.*$')
        s = [comment.sub('', x).strip() for x in s]
        active = True
        c = ''
        line = 0
        for x in s:
            line = line + 1
            if x == '':
                continue
            if x.startswith('++'):
                x = x[2:].split()
                if len(x) == 0:
                    active = True
                    continue
                if self.pandokia_driver_name in x:
                    active = True
                    continue
                active = False
            else:
                if not active:
                    pass
                else:
                    c = c + x + '\n'
                    if c.endswith(';\n'):
                        cursor = self.execute(c)
                        tbl = text_table.text_table()
                        if cursor.description:
                            for name in cursor.description:
                                name = name[0]
                                tbl.define_column(name)

                        try:
                            for rownum, rowval in enumerate(cursor):
                                for colnum, colval in enumerate(rowval):
                                    tbl.set_value(rownum, colnum, colval)

                            if len(tbl.rows) > 0:
                                print(tbl.get(format=format, headings=1))
                        except self.ProgrammingError as e:
                            if 'no results to fetch' in str(e):
                                pass
                            else:
                                print('Programming Error for %s' % c)
                                print(e)
                        except self.IntegrityError as e:
                            print('Integrity Error for %s' % c)
                            print(e)

                        cursor.close()
                        c = ''

        self.commit()


def cmd_dump_table(args):
    import pandokia
    for x in args:
        pandokia.cfg.pdk_db.table_to_csv(x, sys.stdout)


def sql_files(files):
    import os.path, pandokia
    pdk_db = pandokia.cfg.pdk_db
    format = 'tw'
    while len(files) > 0 and files[0].startswith('-'):
        arg = files[0]
        files = files[1:]
        if arg in ('-html', '-csv', '-awk', '-rst', '-text', '-trac_wiki', '-tw'):
            format = arg[1:]
            print('FORMAT %s' % format)
        else:
            print('%s unrecognized' % arg)
            return 1

    if len(files) > 0:
        dir = os.path.dirname(__file__) + '/sql/'
        for x in files:
            try:
                f = open(x)
            except IOError:
                f = open(dir + x)

            pdk_db.sql_commands((f.read()), format=format)
            f.close()

    else:
        pdk_db.sql_commands((sys.stdin.read()), format=format)
    return 0


def db_from_django(settings):
    """Connect to a django database, using the pandokia database interface.

    The parameter is the django settings module.

    This function is useful mainly when you want something from an
    application that uses a django database, but you don't want to go
    through the pain of using the django ORM to form your query.

    """
    if settings.DATABASE_ENGINE == 'mysql':
        import pandokia.db_mysqldb as dbmod
        access = {'host':settings.DATABASE_HOST,  'db':settings.DATABASE_NAME, 
         'user':settings.DATABASE_USER, 
         'passwd':settings.DATABASE_PASSWORD}
        if settings.DATABASE_PORT:
            access['port'] = settings.DATABASE_PORT
        db = dbmod.PandokiaDB(access)
        return db
    if settings.DATABASE_ENGINE == 'sqlite3':
        import pandokia.db_sqlite as dbmod
        db = dbmod.PandokiaDB({'db': settings.DATABASE_NAME})
        return db
    raise Exception('Pandokia does not know django database engine name %s' % settings.DATABASE_ENGINE)