# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/oort/util/templating.py
# Compiled at: 2007-09-30 15:59:05
import pkg_resources
available_engines = dict([ (entry_point.name, entry_point.load()) for entry_point in pkg_resources.iter_entry_points('python.templating.engines')
                         ])

class TemplateEngineManager(object):

    def __init__(self, extra_vars_func=None, engine_opts=None):
        self.extra_vars_func = extra_vars_func
        self.engine_opts = engine_opts
        self.engines = {}

    def get_engine_and_path(self, path, default_engine=None):
        if ':' not in path:
            dotted_path = path
            engine_name = default_engine
        else:
            (engine_name, dotted_path) = path.split(':', 1)
        engine = self._get_engine(engine_name)
        return (engine, dotted_path)

    def render_template(self, path, data, format, fragment=False):
        (engine, dotted_path) = self.get_engine_and_path(path)
        result = engine.render(data, format=format, fragment=fragment, template=dotted_path)
        return result

    def _get_engine(self, engine_name):
        engine = self.engines.get(engine_name)
        if not engine:
            Engine = available_engines.get(engine_name, None)
            if not Engine:
                msg = 'No engine for "%s" found. Please install it.'
                raise TemplateEngineMissing(msg % (engine_name,))
            self.engines[engine_name] = engine = Engine(self.extra_vars_func, self.engine_opts)
        return engine


class TemplateEngineMissing(Exception):
    pass