# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/Cellar/python/2.7.10_2/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/stylus/__init__.py
# Compiled at: 2016-02-01 13:48:12
import os
from os import path
import execjs, io
node_modules = path.abspath('node_modules')
if 'NODE_PATH' not in os.environ:
    os.environ['NODE_PATH'] = node_modules
elif node_modules not in os.environ['NODE_PATH']:
    os.pathsep.join((os.environ['NODE_PATH'], node_modules))

class Stylus(object):

    def __init__(self, compress=False, paths=[], imports=[], plugins={}):
        """
    compress: Whether the resulting css should be compressed.
    paths: List of stylesheet load paths.
    imports: Stylesheets to import on every compile.
    plugins: List of plugins to use.
    """
        self.compress = compress
        self.paths = list(paths)
        self.imports = list(imports)
        self.plugins = dict(plugins)
        self._context = None
        self._backend = None
        return

    def use(self, plugin, arguments={}):
        """Add plugin to use during compilation.

    plugin: Plugin to include.
    arguments: Dictionary of arguments to pass to the import.
    """
        self.plugins[plugin] = dict(arguments)
        return self.plugins

    def compile(self, source, options={}):
        """Compile stylus into css

    source: A string containing the stylus code
    options: A dictionary of arguments to pass to the compiler

    Returns a string of css resulting from the compilation
    """
        options = dict(options)
        if 'paths' in options:
            options['paths'] += self.paths
        else:
            options['paths'] = self.paths
        if 'compress' not in options:
            options['compress'] = self.compress
        return self.context.call('compiler', source, options, self.plugins, self.imports)

    @property
    def context(self):
        """Internal property that returns the stylus compiler"""
        if self._context is None:
            with io.open(path.join(path.abspath(path.dirname(__file__)), 'compiler.js')) as (compiler_file):
                compiler_source = compiler_file.read()
            self._context = self.backend.compile(compiler_source)
        return self._context

    @property
    def backend(self):
        """Internal property that returns the Node script running harness"""
        if self._backend is None:
            with io.open(path.join(path.abspath(path.dirname(__file__)), 'runner.js')) as (runner_file):
                runner_source = runner_file.read()
            self._backend = execjs.ExternalRuntime(name='Node.js (V8)', command=[
             'node'], runner_source=runner_source)
        return self._backend