# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danjac/petprojects/tesla/tests/output/ProjectName/projectname/lib/database.py
# Compiled at: 2007-09-06 07:54:15
import sacontext, elixir

class ElixirStrategy(sacontext.ContextualStrategy):

    def create_session(self, context):
        return elixir.objectstore.session

    def create_metadata(self, key, context):
        elixir.metadata.connect(context.get_engine(key))
        return elixir.metadata

    def get_connectable(self, key, context):
        return context.get_engine(key)


context = sacontext.PylonsSAContext(strategy=ElixirStrategy())

def connect(name=None):
    """
    Connects engine 
    """
    context.add_engine_from_config(name)
    elixir.setup_all()


def resync():
    """
    Renews SQLAlchemy session with current thread
    """
    context.session.clear()


def flush_all():
    """
    Flushes all changes to database
    """
    elixir.objectstore.flush()


def execute(query):
    """
    Executes an SQL query string
    """
    return context.engine.text(query).execute()


def create_all(*args, **kw):
    """
    Shortcut for metadata.create_all()
    """
    context.metadata.create_all(*args, **kw)


def drop_all(*args, **kw):
    """
    Shortcut for metadata.drop_all()
    """
    context.metadata.drop_all(*args, **kw)


def get_context():
    return context