# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/CherrypyElixir/cherrypy_elixir.py
# Compiled at: 2012-12-23 14:24:52
__doc__ = '\nCreated on Jul 12, 2012\n\n@author: vahid\n'
import cherrypy, elixir, sqlalchemy

class ElixirPlugin(cherrypy.process.plugins.SimplePlugin):
    db_uri = None
    echo = False
    convert_unicode = True
    pool_size = 10
    create_tables = True
    engine = None

    def __init__(self, bus):
        cherrypy.process.plugins.SimplePlugin.__init__(self, bus)
        from sqlalchemy.orm import scoped_session, sessionmaker
        elixir.session = scoped_session(sessionmaker(autoflush=True, autocommit=False))
        elixir.options_defaults.update({'shortnames': True})

    def _ensure_engine(self):
        if not self.engine:
            engineParams = {}
            if self.db_uri.startswith('postgresql'):
                engineParams['pool_size'] = self.pool_size
            self.engine = sqlalchemy.create_engine(self.db_uri, echo=self.echo, convert_unicode=self.convert_unicode, **engineParams)

    def start(self):
        self._ensure_engine()
        elixir.metadata.bind = self.engine
        elixir.setup_all(create_tables=self.create_tables)
        self.bus.subscribe('bind_elixir_session', self.bind)

    start.priority = 80

    def stop(self):
        if self.engine:
            self.engine.dispose()
            self.engine = None
        return

    def bind(self, session):
        session.configure(bind=self.engine)


class ElixirTool(cherrypy.Tool):

    def __init__(self):
        cherrypy.Tool.__init__(self, 'on_start_resource', self.on_start_resource, 'elixir', 20)

    @property
    def session(self):
        return elixir.session

    def on_start_resource(self):
        cherrypy.engine.publish('bind_elixir_session', self.session)
        cherrypy.request.db = self.session

    def on_end_resource(self, **kwargs):
        cherrypy.request.db = None
        try:
            try:
                self.session.commit()
            except:
                self.session.rollback()
                raise

        finally:
            self.session.remove()

        return

    def _setup(self):
        if cherrypy.request.config.get('tools.staticdir.on', False) or cherrypy.request.config.get('tools.staticfile.on', False):
            return
        cherrypy.Tool._setup(self)
        cherrypy.request.hooks.attach('on_end_resource', self.on_end_resource)


def setup():
    cherrypy.engine.elixir = ElixirPlugin(cherrypy.engine)
    cherrypy.tools.elixir = ElixirTool()