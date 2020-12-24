# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sql/run.py
# Compiled at: 2020-05-02 10:55:12
# Size of source mod 2**32: 13024 bytes
import codecs, csv, operator, os.path, re
from functools import reduce
import prettytable, six, sqlalchemy, sqlparse
from .column_guesser import ColumnGuesserMixin
try:
    from pgspecial.main import PGSpecial
except ImportError:
    PGSpecial = None
else:

    def unduplicate_field_names(field_names):
        """Append a number to duplicate field names to make them unique. """
        res = []
        for k in field_names:
            if k in res:
                i = 1
                if k + '_' + str(i) in res:
                    i += 1
                else:
                    k += '_' + str(i)
            res.append(k)
        else:
            return res


    class UnicodeWriter(object):
        __doc__ = '\n    A CSV writer which will write rows to CSV file "f",\n    which is encoded in the given encoding.\n    '

        def __init__(self, f, dialect=csv.excel, encoding='utf-8', **kwds):
            self.queue = six.StringIO()
            self.writer = (csv.writer)(self.queue, dialect=dialect, **kwds)
            self.stream = f
            self.encoder = codecs.getincrementalencoder(encoding)()

        def writerow(self, row):
            if six.PY2:
                _row = [s.encode('utf-8') if hasattr(s, 'encode') else s for s in row]
            else:
                _row = row
            self.writer.writerow(_row)
            data = self.queue.getvalue()
            if six.PY2:
                data = data.decode('utf-8')
                data = self.encoder.encode(data)
            self.stream.write(data)
            self.queue.truncate(0)
            self.queue.seek(0)

        def writerows(self, rows):
            for row in rows:
                self.writerow(row)


    class CsvResultDescriptor(object):
        __doc__ = 'Provides IPython Notebook-friendly output for the feedback after a ``.csv`` called.'

        def __init__(self, file_path):
            self.file_path = file_path

        def __repr__(self):
            return 'CSV results at %s' % os.path.join(os.path.abspath('.'), self.file_path)

        def _repr_html_(self):
            return '<a href="%s">CSV results</a>' % os.path.join('.', 'files', self.file_path)


    def _nonbreaking_spaces(match_obj):
        """
    Make spaces visible in HTML by replacing all `` `` with ``&nbsp;``

    Call with a ``re`` match object.  Retain group 1, replace group 2
    with nonbreaking speaces.
    """
        spaces = '&nbsp;' * len(match_obj.group(2))
        return '%s%s' % (match_obj.group(1), spaces)


    _cell_with_spaces_pattern = re.compile('(<td>)( {2,})')

    class ResultSet(list, ColumnGuesserMixin):
        __doc__ = '\n    Results of a SQL query.\n\n    Can access rows listwise, or by string value of leftmost column.\n    '

        def __init__(self, sqlaproxy, sql, config):
            self.keys = sqlaproxy.keys()
            self.sql = sql
            self.config = config
            self.limit = config.autolimit
            style_name = config.style
            self.style = prettytable.__dict__[style_name.upper()]
            if sqlaproxy.returns_rows:
                if self.limit:
                    list.__init__(self, sqlaproxy.fetchmany(size=(self.limit)))
                else:
                    list.__init__(self, sqlaproxy.fetchall())
                self.field_names = unduplicate_field_names(self.keys)
                self.pretty = PrettyTable((self.field_names), style=(self.style))
            else:
                list.__init__(self, [])
                self.pretty = None

        def _repr_html_(self):
            _cell_with_spaces_pattern = re.compile('(<td>)( {2,})')
            if self.pretty:
                self.pretty.add_rows(self)
                result = self.pretty.get_html_string()
                result = _cell_with_spaces_pattern.sub(_nonbreaking_spaces, result)
                if self.config.displaylimit:
                    if len(self) > self.config.displaylimit:
                        result = '%s\n<span style="font-style:italic;text-align:center;">%d rows, truncated to displaylimit of %d</span>' % (
                         result, len(self), self.config.displaylimit)
                return result
            return

        def __str__(self, *arg, **kwarg):
            self.pretty.add_rows(self)
            return str(self.pretty or '')

        def __getitem__--- This code section failed: ---

 L. 149         0  SETUP_FINALLY        16  'to 16'

 L. 150         2  LOAD_GLOBAL              list
                4  LOAD_METHOD              __getitem__
                6  LOAD_FAST                'self'
                8  LOAD_DEREF               'key'
               10  CALL_METHOD_2         2  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 151        16  DUP_TOP          
               18  LOAD_GLOBAL              TypeError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE   104  'to 104'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 152        30  LOAD_CLOSURE             'key'
               32  BUILD_TUPLE_1         1 
               34  LOAD_LISTCOMP            '<code_object <listcomp>>'
               36  LOAD_STR                 'ResultSet.__getitem__.<locals>.<listcomp>'
               38  MAKE_FUNCTION_8          'closure'
               40  LOAD_FAST                'self'
               42  GET_ITER         
               44  CALL_FUNCTION_1       1  ''
               46  STORE_FAST               'result'

 L. 153        48  LOAD_FAST                'result'
               50  POP_JUMP_IF_TRUE     60  'to 60'

 L. 154        52  LOAD_GLOBAL              KeyError
               54  LOAD_DEREF               'key'
               56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            50  '50'

 L. 155        60  LOAD_GLOBAL              len
               62  LOAD_FAST                'result'
               64  CALL_FUNCTION_1       1  ''
               66  LOAD_CONST               1
               68  COMPARE_OP               >
               70  POP_JUMP_IF_FALSE    92  'to 92'

 L. 156        72  LOAD_GLOBAL              KeyError
               74  LOAD_STR                 '%d results for "%s"'
               76  LOAD_GLOBAL              len
               78  LOAD_FAST                'result'
               80  CALL_FUNCTION_1       1  ''
               82  LOAD_DEREF               'key'
               84  BUILD_TUPLE_2         2 
               86  BINARY_MODULO    
               88  CALL_FUNCTION_1       1  ''
               90  RAISE_VARARGS_1       1  'exception instance'
             92_0  COME_FROM            70  '70'

 L. 157        92  LOAD_FAST                'result'
               94  LOAD_CONST               0
               96  BINARY_SUBSCR    
               98  ROT_FOUR         
              100  POP_EXCEPT       
              102  RETURN_VALUE     
            104_0  COME_FROM            22  '22'
              104  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 26

        def dict(self):
            """Returns a single dict built from the result set

        Keys are column names; values are a tuple"""
            return dict(zip(self.keys, zip(*self)))

        def dicts(self):
            """Iterator yielding a dict for each row"""
            for row in self:
                (yield dict(zip(self.keys, row)))

        def DataFrame(self):
            """Returns a Pandas DataFrame instance built from the result set."""
            import pandas as pd
            frame = pd.DataFrame(self, columns=(self and self.keys or []))
            return frame

        def pie(self, key_word_sep=' ', title=None, **kwargs):
            """Generates a pylab pie chart from the result set.

        ``matplotlib`` must be installed, and in an
        IPython Notebook, inlining must be on::

            %%matplotlib inline

        Values (pie slice sizes) are taken from the
        rightmost column (numerical values required).
        All other columns are used to label the pie slices.

        Parameters
        ----------
        key_word_sep: string used to separate column values
                      from each other in pie labels
        title: Plot title, defaults to name of value column

        Any additional keyword arguments will be passsed
        through to ``matplotlib.pylab.pie``.
        """
            self.guess_pie_columns(xlabel_sep=key_word_sep)
            import matplotlib.pylab as plt
            pie = (plt.pie)(self.ys[0], labels=self.xlabels, **kwargs)
            plt.title(title or self.ys[0].name)
            return pie

        def plot(self, title=None, **kwargs):
            """Generates a pylab plot from the result set.

        ``matplotlib`` must be installed, and in an
        IPython Notebook, inlining must be on::

            %%matplotlib inline

        The first and last columns are taken as the X and Y
        values.  Any columns between are ignored.

        Parameters
        ----------
        title: Plot title, defaults to names of Y value columns

        Any additional keyword arguments will be passsed
        through to ``matplotlib.pylab.plot``.
        """
            import matplotlib.pylab as plt
            self.guess_plot_columns()
            self.x = self.x or range(len(self.ys[0]))
            coords = reduce(operator.add, [(self.x, y) for y in self.ys])
            plot = (plt.plot)(*coords, **kwargs)
            if hasattr(self.x, 'name'):
                plt.xlabel(self.x.name)
            ylabel = ', '.join((y.name for y in self.ys))
            plt.title(title or ylabel)
            plt.ylabel(ylabel)
            return plot

        def bar(self, key_word_sep=' ', title=None, **kwargs):
            """Generates a pylab bar plot from the result set.

        ``matplotlib`` must be installed, and in an
        IPython Notebook, inlining must be on::

            %%matplotlib inline

        The last quantitative column is taken as the Y values;
        all other columns are combined to label the X axis.

        Parameters
        ----------
        title: Plot title, defaults to names of Y value columns
        key_word_sep: string used to separate column values
                      from each other in labels

        Any additional keyword arguments will be passsed
        through to ``matplotlib.pylab.bar``.
        """
            import matplotlib.pylab as plt
            self.guess_pie_columns(xlabel_sep=key_word_sep)
            plot = (plt.bar)((range(len(self.ys[0]))), (self.ys[0]), **kwargs)
            if self.xlabels:
                plt.xticks((range(len(self.xlabels))), (self.xlabels), rotation=45)
            plt.xlabel(self.xlabel)
            plt.ylabel(self.ys[0].name)
            return plot

        def csv(self, filename=None, **format_params):
            """Generate results in comma-separated form.  Write to ``filename`` if given.
           Any other parameters will be passed on to csv.writer."""
            if not self.pretty:
                return
            else:
                self.pretty.add_rows(self)
                if filename:
                    encoding = format_params.get('encoding', 'utf-8')
                    if six.PY2:
                        outfile = open(filename, 'wb')
                    else:
                        outfile = open(filename, 'w', newline='', encoding=encoding)
                else:
                    outfile = six.StringIO()
            writer = UnicodeWriter(outfile, **format_params)
            writer.writerow(self.field_names)
            for row in self:
                writer.writerow(row)
            else:
                if filename:
                    outfile.close()
                    return CsvResultDescriptor(filename)
                return outfile.getvalue()


    def interpret_rowcount(rowcount):
        if rowcount < 0:
            result = 'Done.'
        else:
            result = '%d rows affected.' % rowcount
        return result


    class FakeResultProxy(object):
        __doc__ = 'A fake class that pretends to behave like the ResultProxy from\n    SqlAlchemy.\n    '

        def __init__(self, cursor, headers):
            if cursor is None:
                cursor = []
                headers = []
            elif isinstance(cursor, list):
                self.from_list(source_list=cursor)
            else:
                self.fetchall = cursor.fetchall
                self.fetchmany = cursor.fetchmany
                self.rowcount = cursor.rowcount
            self.keys = lambda : headers
            self.returns_rows = True

        def from_list(self, source_list):
            """Simulates SQLA ResultProxy from a list."""
            self.fetchall = lambda : source_list
            self.rowcount = len(source_list)

            def fetchmany(size):
                pos = 0
                while pos < len(source_list):
                    (yield source_list[pos:pos + size])
                    pos += size

            self.fetchmany = fetchmany


    _COMMIT_BLACKLIST_DIALECTS = ('mssql', 'clickhouse', 'teradata', 'athena')

    def _commit(conn, config):
        """Issues a commit, if appropriate for current config and dialect"""
        _should_commit = config.autocommit and all((dialect not in str(conn.dialect) for dialect in _COMMIT_BLACKLIST_DIALECTS))
        if _should_commit:
            try:
                conn.session.execute('commit')
            except sqlalchemy.exc.OperationalError:
                pass


    def run(conn, sql, config, user_namespace):
        if sql.strip():
            for statement in sqlparse.split(sql):
                first_word = sql.strip().split()[0].lower()
                if first_word == 'begin':
                    raise Exception('ipython_sql does not support transactions')
                if first_word.startswith('\\') and 'postgres' in str(conn.dialect):
                    if not PGSpecial:
                        raise ImportError('pgspecial not installed')
                    pgspecial = PGSpecial()
                    _, cur, headers, _ = pgspecial.execute(conn.session.connection.cursor(), statement)[0]
                    result = FakeResultProxy(cur, headers)
                else:
                    txt = sqlalchemy.sql.text(statement)
                    result = conn.session.execute(txt, user_namespace)
                _commit(conn=conn, config=config)
                if result:
                    if config.feedback:
                        print(interpret_rowcount(result.rowcount))
                    resultset = ResultSet(result, statement, config)
                    if config.autopandas:
                        return resultset.DataFrame()
                    return resultset

        else:
            return 'Connected: %s' % conn.name


    class PrettyTable(prettytable.PrettyTable):

        def __init__(self, *args, **kwargs):
            self.row_count = 0
            self.displaylimit = None
            return (super(PrettyTable, self).__init__)(*args, **kwargs)

        def add_rows(self, data):
            if self.row_count:
                if data.config.displaylimit == self.displaylimit:
                    return
            else:
                self.clear_rows()
                self.displaylimit = data.config.displaylimit
                if self.displaylimit == 0:
                    self.displaylimit = None
                if self.displaylimit in (None, 0):
                    self.row_count = len(data)
                else:
                    self.row_count = min(len(data), self.displaylimit)
            for row in data[:self.displaylimit]:
                self.add_row(row)