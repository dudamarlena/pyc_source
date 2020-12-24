# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\command\sacommand.py
# Compiled at: 2011-07-14 07:47:21
from peak.rules import abstract, when, around
from turbogears import config
from turbogears.util import get_model
try:
    from sqlalchemy import MetaData, exceptions, Table, String, Unicode
    from turbogears.database import bind_metadata, metadata, get_engine
except ImportError:
    from turbogears.util import missing_dependency_error
    no_sqlalchemy = missing_dependency_error('SQLAlchemy')
else:
    from sqlalchemy import Text, UnicodeText
    no_sqlalchemy = False

@abstract()
def sacommand(command, args):
    pass


@around(sacommand, "command and command != 'help' and no_sqlalchemy")
def no_engine(command, args):
    print no_sqlalchemy


@when(sacommand, "command == 'help'")
def help(command, args):
    print 'TurboGears SQLAlchemy Helper\n\ntg-admin sql command [options]\n\nAvailable commands:\n    create  Create tables\n    execute Execute SQL statements\n    help    Show help\n    list    List tables that appear in the model\n    status  Show differences between model and database\n'


@when(sacommand, "command == 'create'")
def create(command, args):
    print 'Creating tables at %s' % config.get('sqlalchemy.dburi')
    bind_metadata()
    get_model()
    metadata.create_all()


@when(sacommand, "command == 'list'")
def list_(command, args):
    get_model()
    for tbl in metadata.tables.values():
        print tbl.fullname


@when(sacommand, "command == 'execute'")
def execute(command, args):
    eng = get_engine()
    for cmd in args[2:]:
        ret = eng.execute(cmd)
        try:
            print list(ret)
        except:
            pass


@when(sacommand, "command == 'status'")
def status(command, args):
    bind_metadata()
    get_model()
    ret = compare_metadata(metadata, MetaData(metadata.bind))
    for l in ret:
        print l

    if not ret:
        print 'Database matches model'


def indent(ls):
    return [ '    ' + l for l in ls ]


def compare_metadata(pym, dbm):
    rc = []
    for pyt in pym.tables.values():
        try:
            dbt = Table(pyt.name, dbm, autoload=True, schema=pyt.schema)
        except exceptions.NoSuchTableError:
            rc.extend(('Create table ' + pyt.fullname, ''))
        else:
            ret = compare_table(pyt, dbt)
            if ret:
                rc.append('Change table ' + pyt.fullname)
                rc.extend(indent(ret) + [''])

    return rc


def compare_table(pyt, dbt):
    rc = []
    dbcols = dict([ (s.lower(), s) for s in dbt.columns.keys() ])
    for pyc in pyt.columns:
        name = pyc.name.lower()
        if name in dbcols:
            ret = compare_column(pyc, dbt.columns[dbcols[name]])
            if ret:
                rc.append('Change column ' + pyc.name)
                rc.extend(indent(ret))
            dbcols.pop(name)
        else:
            rc.append('Add column ' + pyc.name)

    for dbcol in dbcols:
        rc.append('Remove column ' + dbcol)

    return rc


def compare_column(pyc, dbc):
    rc = []
    pyt, dbt = pyc.type, dbc.type
    if isinstance(pyt, Unicode):
        pyt = String(pyt.length)
    elif isinstance(pyt, UnicodeText):
        pyt = Text(pyt.length)
    if not isinstance(dbt, pyt.__class__):
        rc.append('Change type to ' + pyt.__class__.__name__)
    elif isinstance(pyt, String):
        if pyt.length != dbt.length:
            rc.append('Change length to ' + str(pyt.length))
    if dbc.primary_key != pyc.primary_key:
        rc.append(pyc.primary_key and 'Make primary key' or 'Remove primary key')
    if dbc.default is not None and pyc.default is not None and dbc.default != pyc.default:
        rc.append('Change default to ' + str(pyc.default.arg))
    if dbc.index is not None and dbc.index != pyc.index:
        rc.append(pyc.index and 'Add index' or 'Remove index')
    return rc