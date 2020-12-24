# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sqlpython/dbapiext.py
# Compiled at: 2012-05-26 21:28:24
"""
An extention to DBAPI-2.0 for more easily building SQL statements.

This extension allows you to call a DBAPI Cursor's execute method with a string
that contains format specifiers for escaped and/or unescaped arguments.  Escaped
arguments are specified using `` %X `` or `` %S `` (capital X or capital S).
You can also mix positional and keyword arguments in the call, and this takes
advantage of the Python call syntax niceties.  Also, lists passed in as
parameters to be formatted are automatically detected and joined by commas (this
works for both unescaped and escaped parameters-- lists to be escaped have their
elements escaped individually).  In addition, if you pass in a dictionary
corresponding to an escaped formatting specifier, the dictionary is rendered as
a list of comma-separated <key> = <value> pairs, such as are suitable for an
INSERT statement.

For performance, the results of analysing and preparing the query is kept in a
cache and reused on subsequence calls, similarly to the re or struct library.

(This is intended to become a reference implementation for a proposal for an
extension to tbe DBAPI-2.0.)

.. note:: for now the transformation only works with DBAPIs that supports
          parametric arguments in the form of Python's syntax for now
          (e.g. psycopg2).  It could easily be extended to support other DBAPI
          syntaxes.

For more details and motivation, see the accompanying explanation document at
http://furius.ca/pubcode/pub/conf/common/lib/python/dbapiext.html

5-minute usage instructions:

  Run execute_f() with a cursor object and appropriate arguments::

    execute_f(cursor, ' SELECT %s FROM %(t)s WHERE id = %S ', cols, id, t=table)

  Ideally, we should be able to monkey-patch this method onto the cursor class
  of the DBAPI library (this may not be possible if it is an extension module).

  By default, the result of analyzing each query is cached automatically and
  reused on further invocations, to minimize the amount of analysis to be
  performed at runtime.  If you want to do this explicitly, first compile your
  query, and execute it later with the resulting object, e.g.::

    analq = qcompile(' SELECT %s FROM %(t)s WHERE id = %S ')
    ...
    analq.execute(cursor, cols, id, t=table)

**Note to developers: this module contains tests, if you make any changes,
please make sure to run and fix the tests.**

Also, a formatting specifier is provided for where clauses: ``%A``, which joins
its contained entries with ``AND``. The only accepted data types are list of
pairs or a dictionary. Maybe we could provide an OR version (``%A`` and
``%O``).

Future Work
===========

- We could provide a reduce() method on the QueryAnalyzer, that will apply the
  given parameters and save the calculated arguments for later use; This would
  allow us to apply queries using multiple calls, to fill in only certain
  parameters at a time.  This method would return a new QueryAnalyzer, albeit
  one that would contain some pre-cooked apply_kwds and delay_kwds to be
  accumulated to in the apply call.

- Provide a simple test function that would allow people to test their queries
  without having to create a TestCursor.

"""
import re
from itertools import starmap, imap
from StringIO import StringIO
from datetime import date, datetime
from itertools import izip, count
from pprint import pprint
__all__ = (
 'execute_f', 'qcompile', 'set_paramstyle', 'execute_obj')

class QueryAnalyzer(object):
    """
    Analyze and contain a query string in a way that we can quickly put it back
    together when given the actual arguments.  This object contains knowledge of
    which arguments are positional and keyword, and is able to conditionally
    apply escaping when necessary, and expand lists as well.

    This is meant to be kept around or cached for efficiency.
    """
    re_fmt = '[#0 +-]?([0-9]+|\\*)?(\\.[0-9]*)?[hlL]?[diouxXeEfFgGcrsSAO]'
    regexp = re.compile('%%(\\(([a-zA-Z0-9_]+)\\))?(%s)' % re_fmt)

    def __init__(self, query, paramstyle=None):
        global _def_paramstyle
        self.orig_query = query
        self.positional = []
        self.components = None
        if paramstyle is None:
            paramstyle = _def_paramstyle
        self.paramstyle = paramstyle
        self.init_style(paramstyle)
        self.analyze()
        return

    def init_style(self, paramstyle):
        """Pre-calculate style-specific constants."""
        if paramstyle == 'pyformat':
            self.style_fmt = '%%%%(%(name)s)s'
            self.style_argstype = dict
        elif paramstyle == 'named':
            self.style_fmt = ':%(name)s'
            self.style_argstype = dict
        elif paramstyle == 'qmark':
            self.style_fmt = '?'
            self.style_argstype = list
        elif paramstyle == 'format':
            self.style_fmt = '%%%%s'
            self.style_argstype = list
        elif paramstyle == 'numeric':
            self.style_fmt = ':%(no)d'
            self.style_argstype = list
        elif paramstyle == 'atnamed':
            self.style_fmt = '@%(name)s'
            self.style_argstype = dict
        else:
            raise ValueError("Parameter style '%s' is not supported." % paramstyle)

    def analyze(self):
        query = self.orig_query
        poscount = count(1)
        comps = self.components = []
        for x in gensplit(self.regexp, query):
            if isinstance(x, (str, unicode)):
                comps.append(x)
            else:
                keyname, fmt = x.group(2, 3)
                if keyname is None:
                    keyname = '__p%d' % poscount.next()
                    self.positional.append(keyname)
                sep = ', '
                if fmt in 'XS':
                    fmt = 's'
                    escaped = True
                elif fmt in 'A':
                    fmt = 's'
                    escaped = True
                    sep = ' AND '
                elif fmt in 'O':
                    fmt = 's'
                    escaped = True
                    sep = ' OR '
                else:
                    escaped = False
                comps.append((keyname, escaped, sep, fmt))

        return

    def __str__(self):
        """
        Return the string that would be used before application of the
        positional and keyword arguments.
        """
        style_fmt = self.style_fmt
        oss = StringIO()
        no = count(1)
        for x in self.components:
            if isinstance(x, (str, unicode)):
                oss.write(x)
            else:
                keyname, escaped, sep, fmt = x
                if escaped:
                    oss.write(style_fmt % {'name': keyname, 'no': no.next()})
                else:
                    oss.write('%%(%s)%s' % (keyname, fmt))

        return oss.getvalue()

    def apply(self, *args, **kwds):
        if len(args) != len(self.positional):
            raise TypeError('not enough arguments for format string')
        for name, value in izip(self.positional, args):
            assert name not in kwds
            kwds[name] = value

        listexpans = {}
        apply_kwds, delay_kwds = {}, self.style_argstype()
        no = count(1)
        style_fmt = self.style_fmt
        dict_fmt = '%%(key)s = %s' % style_fmt
        output = []
        for x in self.components:
            if isinstance(x, (str, unicode)):
                out = x
            else:
                keyname, escaped, sep, fmt = x
                value = kwds[keyname]
                if isinstance(value, (tuple, list, set)):
                    try:
                        words = listexpans[keyname]
                    except KeyError:
                        words = [ '%s_l%d__' % (keyname, x) for x in xrange(len(value)) ]
                        listexpans[keyname] = words

                    if escaped:
                        outfmt = [ style_fmt % {'name': x, 'no': no.next()} for x in words ]
                    else:
                        outfmt = [ '%%(%s)%s' % (x, fmt) for x in words ]
                elif isinstance(value, dict):
                    if not escaped:
                        raise ValueError('Attempting to format a dict in an SQL statement without escaping.')
                    items = value.items()
                    words = [ '%s_key_%s__' % (keyname, x[0]) for x in items ]
                    value = [ x[1] for x in items ]
                    outfmt = [ dict_fmt % {'key': k, 'name': word} for word, (k, v) in izip(words, items)
                             ]
                else:
                    words, value = (
                     keyname,), (value,)
                    if escaped:
                        outfmt = [
                         style_fmt % {'name': keyname, 'no': no.next()}]
                    else:
                        outfmt = [
                         '%%(%s)%s' % (keyname, fmt)]
                if escaped:
                    okwds = delay_kwds
                else:
                    okwds = apply_kwds
                assert len(words) == len(value)
                if isinstance(okwds, dict):
                    okwds.update(izip(words, value))
                else:
                    okwds.extend(value)
                out = sep.join(outfmt)
            output.append(out)

        newquery = ('').join(output)
        return (
         newquery % apply_kwds, delay_kwds)

    def execute(self, cursor_, *args, **kwds):
        """
        Execute the analyzed query on the given cursor, with the given arguments
        and keywords.
        """
        cquery, ckwds = self.apply(*args, **kwds)
        return cursor_.execute(cquery, ckwds)


def gensplit(regexp, s):
    """
    Regexp-splitter generator.  Generates strings and match objects.
    """
    c = 0
    for mo in regexp.finditer(s):
        yield s[c:mo.start()]
        yield mo
        c = mo.end()

    yield s[c:]


_def_paramstyle = 'pyformat'

def set_paramstyle(style_or_dbapi):
    """
    Sets the default paramstyle to be used by the underlying DBAPI.
    You can pass in a DBAPI module object or a string. See PEP249 for details.
    """
    global _def_paramstyle
    if isinstance(style_or_dbapi, str):
        _def_paramstyle = style_or_dbapi
    else:
        _def_paramstyle = style_or_dbapi.paramstyle
    assert _def_paramstyle in ('qmark', 'numeric', 'named', 'format', 'pyformat')


qcompile = QueryAnalyzer
_query_cache = {}

def execute_f(cursor_, query_, *args, **kwds):
    """
    Fancy execute method for a cursor.  (Note: this is implemented as a function
    but is really meant to be a method to replace or complement the standard
    method Cursor.execute() from DBAPI-2.0.)

    Convert fancy query arguments into a DBAPI-compatible set of arguments and
    execute.

    This method supports a different syntax than the DBAPI execute() method:

    - By default, %s placeholders are not escaped.

    - Use the %S or %(name)S placeholder to specify escaped strings.

    - You can specify positional arguments without having to place them in an
      extra tuple.

    - Keyword arguments are used as expected to fill in missing values.
      Positional arguments are used to fill non-keyword placeholders.

    - Arguments that are tuples, lists or sets will be automatically joined by colons.
      If the corresponding formatting is %S or %(name)S, the members of the
      sequence will be escaped individually.

    See qcompile() for details.

    Note that this function accepts a '_paramstyle' optional argument, to set
    which parameter style to use.
    """
    debug = debug_convert or kwds.pop('__debug__', None)
    if debug:
        print '\n' + '=' * 80
        print '\noriginal ='
        print query_
        print '\nargs ='
        pprint(args)
        print '\nkwds ='
        pprint(kwds)
    try:
        q = _query_cache[query_]
    except KeyError:
        _query_cache[query_] = q = qcompile(query_, paramstyle=kwds.pop('paramstyle', None))

    if debug:
        print '\nquery analyzer =', str(q)
    cquery, ckwds = q.apply(*args, **kwds)
    if debug:
        print '\ntransformed ='
        print cquery
        print '\nnewkwds ='
        pprint(ckwds)
    return cursor_.execute(cquery, ckwds)


try:
    from collections import namedtuple
    from collections import _iskeyword
    not_alphanumeric = re.compile('[^a-zA-Z0-9]')

    def rename_duplicates(lst, append_char='_'):
        newlist = []
        for itm in lst:
            while itm in newlist:
                itm += append_char

            newlist.append(itm)

        return newlist


    def _fix_fieldname(fieldname):
        """Ensure that a field name will pass collection.namedtuple's criteria."""
        fieldname = not_alphanumeric.sub('_', fieldname)
        while _iskeyword(fieldname):
            fieldname = fieldname + '_'

        return fieldname


    def ntuple(typename, field_names, verbose=False):
        field_names = [ _fix_fieldname(fn) for fn in field_names.split() ]
        field_names = rename_duplicates(field_names)
        return namedtuple(typename, (' ').join(field_names), verbose)


except ImportError:
    ntuple = None

if ntuple:
    from operator import itemgetter

    def execute_obj(conn, *args, **kwds):
        """
        Run a query on the given connection or cursor and yield ntuples of the
        results.  'curs' can be either a Connection or a Cursor object.
        """
        if re.search('Cursor', conn.__class__.__name__, re.I):
            curs = conn
        else:
            curs = conn.cursor()
        execute_f(curs, *args, **kwds)
        names = map(itemgetter(0), curs.description)
        TupleCls = ntuple('Row', (' ').join(names))
        return starmap(TupleCls, imap(tuple, curs))


else:
    execute_obj = None

class _TestCursor(object):
    """
    Fake cursor that fakes the escaped replacments like a real DBAPI cursor, but
    simply returns the final string.
    """
    execute_f = execute_f

    def execute(self, query, args):
        return self.render_fake(query, args).strip()

    @staticmethod
    def render_fake(query, kwds):
        """
        Take arguments as the DBAPI of execute() accepts and fake escaping the
        arguments as the DBAPI implementation would and return the resulting
        string.  This is used only for testing, to make testing easier and more
        intuitive, to view the completed queries without the replacement
        variables.
        """
        for key, value in kwds.items():
            if isinstance(value, type(None)):
                kwds[key] = 'NULL'
            elif isinstance(value, str):
                kwds[key] = repr(value)
            elif isinstance(value, unicode):
                kwds[key] = repr(value.encode('utf-8'))
            elif isinstance(value, (date, datetime)):
                kwds[key] = repr(value.isoformat())

        result = query % kwds
        if debug_convert:
            print '\n--- 5. after full replacement (fake dbapi application)'
            print result
        return result


def _multi2one(s):
    """Join a multi-line string in a single line."""
    s = re.sub('[ \n]+', ' ', s).strip()
    return re.sub(', ', ',', s)


import unittest

class TestExtension(unittest.TestCase):
    """
    Tests for the extention functions.
    """

    def compare_nows(self, s1, s2):
        """
        Compare two strings without considering the whitespace.
        """
        s1 = _multi2one(s1)
        s2 = _multi2one(s2)
        self.assertEquals(s1, s2)

    def test_basic(self):
        """Basic replacement tests."""
        cursor = _TestCursor()
        simple, isimple, seq = 'SIMPLE', 42, ('L1', 'L2', 'L3')
        for query, args, kwds, expect in (
         (
          ' %s ', (simple,), dict(), ' SIMPLE '),
         (
          ' %S ', (simple,), dict(), " 'SIMPLE' "),
         (
          ' %X ', (simple,), dict(), " 'SIMPLE' "),
         (
          ' %d ', (isimple,), dict(), ' 42 '),
         (
          ' %(k)s ', (), dict(k=simple), ' SIMPLE '),
         (
          ' %(k)d ', (), dict(k=isimple), ' 42 '),
         (
          ' %(k)S ', (), dict(k=simple), " 'SIMPLE' "),
         (
          ' %(k)X ', (), dict(k=simple), " 'SIMPLE' "),
         (
          ' %s ', (seq,), dict(), ' L1,L2,L3 '),
         (
          ' %S ', (seq,), dict(), " 'L1','L2','L3' "),
         (
          ' %X ', (seq,), dict(), " 'L1','L2','L3' "),
         (
          ' %(k)s ', (), dict(k=seq), ' L1,L2,L3 '),
         (
          ' %(k)S ', (), dict(k=seq), " 'L1','L2','L3' "),
         (
          ' %(k)X ', (), dict(k=seq), " 'L1','L2','L3' ")):
            self.compare_nows(cursor.execute_f(query, *args, **kwds), expect)
            self.compare_nows(cursor.execute_f((query + query), *(args + args), **kwds), expect + expect)

    def test_misc(self):
        d = date(2006, 7, 28)
        cursor = _TestCursor()
        self.compare_nows(cursor.execute_f('\n              INSERT INTO %(table)s (%s)\n                SET VALUES (%S)\n                WHERE id = %(id)S\n                  AND name IN (%(name)S)\n                  AND name NOT IN (%(name)S)\n            ', ('col1',
                                                                                                                                                                                                                                                                    'col2'), (42,
                                                                                                                                                                                                                                                                              'bli'), id='02351440-7b7e-4260', name=[
         45, 56, 67, 78], table='table'), "\n              INSERT INTO table (col1, col2)\n                SET VALUES (42, 'bli')\n                WHERE id = '02351440-7b7e-4260'\n                  AND name IN (45, 56, 67, 78)\n                  AND name NOT IN (45, 56, 67, 78)\n              ")
        self.compare_nows(cursor.execute_f(' %(id)s AND %(id)S ', id=[
         'fulano', 'mengano']), " fulano,mengano AND 'fulano','mengano' ")
        self.compare_nows(cursor.execute_f('\n              SELECT %s FROM %s WHERE id = %S\n            ', ('id',
                                                                                                             'name',
                                                                                                             'title'), 'books', '02351440-7b7e-4260'), "SELECT id,name,title FROM books\n               WHERE id = '02351440-7b7e-4260'")
        self.compare_nows(cursor.execute_f('\n           SELECT %s FROM %s WHERE id = %(id)S %(id)S\n        ', ('id',
                                                                                                                 'name',
                                                                                                                 'title'), 'books', id=d), "SELECT id,name,title FROM books\n               WHERE id = '2006-07-28' '2006-07-28'")
        self.compare_nows(cursor.execute_f(' %(id)S %(id)S ', id='02351440-7b7e-4260'), " '02351440-7b7e-4260' '02351440-7b7e-4260' ")
        self.compare_nows(cursor.execute_f(' %s %(id)S %(id)s ', 'books', id='02351440-7b7e-4260'), "  books '02351440-7b7e-4260' 02351440-7b7e-4260  ")
        self.compare_nows(cursor.execute_f('\n              SELECT %s FROM %(table)s WHERE col1 = %S AND col2 < %(val)S\n            ', ('col1',
                                                                                                                                         'col2',
                                                                                                                                         'col3'), 'value1', table='my-table', val=42), " SELECT col1,col2,col3 FROM my-table\n                WHERE col1 = 'value1' AND col2 < 42 ")
        self.compare_nows(cursor.execute_f('\n              INSERT INTO thumbnails\n                (basename, photo1, photo2, photo3)\n                VALUES (%S, %S)\n                ', 'PHOTONAME', ('BIN1',
                                                                                                                                                                                                          'BIN2',
                                                                                                                                                                                                          'BIN3')), "\n              INSERT INTO thumbnails\n                (basename, photo1, photo2, photo3)\n                VALUES ('PHOTONAME', 'BIN1', 'BIN2', 'BIN3')\n                ")

    def test_null(self):
        cursor = _TestCursor()
        self.compare_nows(cursor.execute_f('\n              INSERT INTO poodle (hair)\n                SET VALUES (%S)\n            ', None), '\n              INSERT INTO poodle (hair)\n                SET VALUES (NULL)\n              ')
        return

    def test_paramstyles(self):
        d = date(2006, 7, 28)
        cursor = _TestCursor()
        query = '\n              Simple: %s  Escaped: %S\n              Kwd: %(bli)s KwdEscaped: %(bli)S\n            '
        args = ('hansel', 'gretel')
        kwds = dict(bli='bethel')
        test_data = {'pyformat': (
                      '\n              Simple: hansel  Escaped: %(__p2)s\n              Kwd: bethel KwdEscaped: %(bli)s\n            ', {'__p2': 'gretel', 'bli': 'bethel'}), 
           'named': (
                   '\n              Simple: hansel  Escaped: :__p2\n              Kwd: bethel KwdEscaped: :bli\n            ', {'__p2': 'gretel', 'bli': 'bethel'}), 
           'qmark': (
                   '\n              Simple: hansel  Escaped: ?\n              Kwd: bethel KwdEscaped: ?\n            ', ['gretel', 'bethel']), 
           'format': (
                    '\n              Simple: hansel  Escaped: %s\n              Kwd: bethel KwdEscaped: %s\n            ', ['gretel', 'bethel']), 
           'numeric': (
                     '\n              Simple: hansel  Escaped: :1\n              Kwd: bethel KwdEscaped: :2\n            ', ['gretel', 'bethel'])}
        for style, (estr, eargs) in test_data.iteritems():
            qstr, qargs = qcompile(query, paramstyle=style).apply(*args, **kwds)
            self.compare_nows(qstr, estr)
            self.assertEquals(qargs, eargs)

        print_it = 0
        for style in test_data.iterkeys():
            qanal = qcompile('\n              %S %(c1)S %S %S %(c2)S\n            ', paramstyle=style)
            qstr, qargs = qanal.apply(1, 2, 3, c1='CC1', c2='CC2')
            if print_it:
                print qstr
                print qargs

    def test_dict(self):
        """Tests for passing in a dictionary argument."""
        cursor = _TestCursor()
        data = {'brazil': 'portuguese', 'peru': 'spanish', 
           'japan': 'japanese', 
           'philipines': 'tagalog'}
        self.assertRaises(ValueError, execute_f, cursor, ' unescaped: %s ', data)
        res = execute_f(cursor, ' UPDATE %s SET %S; ', 'mytable', data)
        self.compare_nows(res, "\n           UPDATE mytable\n             SET brazil = 'portuguese',\n                 japan = 'japanese',\n                 philipines = 'tagalog',\n                 peru = 'spanish';       ")

    def test_and(self):
        """Tests for passing in a dictionary argument."""
        cursor = _TestCursor()
        keydata = {'udid': '11111111111111111111', 'imgid': 17}
        valuedata = {'rating': 9}
        self.assertRaises(ValueError, execute_f, cursor, ' unescaped: %s ', keydata)
        res = execute_f(cursor, ' UPDATE %s SET %S WHERE %A; ', 'mytable', valuedata, keydata)
        self.compare_nows(res, "\n           UPDATE mytable\n             SET rating = 9\n             WHERE udid = '11111111111111111111' AND imgid = 17;\n        ")
        res = execute_f(cursor, ' UPDATE %s SET %S WHERE %O; ', 'mytable', valuedata, keydata)
        self.compare_nows(res, "\n           UPDATE mytable\n             SET rating = 9\n             WHERE udid = '11111111111111111111' OR imgid = 17;\n        ")

    def test_sqlite3(self):
        import sqlite3 as dbapi
        set_paramstyle(dbapi)
        conn = dbapi.connect(':memory:')
        curs = conn.cursor()
        execute_f(curs, '\n           CREATE TABLE books (\n              author TEXT,\n              title TEXT,\n              PRIMARY KEY (title)\n           );\n        ')
        execute_f(curs, '\n           INSERT INTO books VALUES (%S);\n        ', ('Tolstoy',
                                                                                  'War and Peace'))
        execute_f(curs, '\n           INSERT INTO books (author) VALUES (%S);\n        ', 'Dostoyesvki')


debug_convert = 0
if __name__ == '__main__':
    unittest.main()