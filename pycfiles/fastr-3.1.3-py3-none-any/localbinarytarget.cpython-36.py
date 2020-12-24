# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/targetplugins/localbinarytarget.py
# Compiled at: 2019-06-04 03:32:43
# Size of source mod 2**32: 11462 bytes
"""
The module containing the classes describing the targets.
"""
import os, platform, subprocess
from typing import List
import fastr
from fastr import exceptions
from fastr.core.target import SubprocessBasedTarget, TargetResult
from fastr.data import url
try:
    from fastr.execution.environmentmodules import EnvironmentModules
    ENVIRONMENT_MODULES = EnvironmentModules(fastr.config.protected_modules)
    ENVIRONMENT_MODULES_LOADED = True
except exceptions.FastrValueError:
    ENVIRONMENT_MODULES = None
    ENVIRONMENT_MODULES_LOADED = False

class LocalBinaryTarget(SubprocessBasedTarget):
    __doc__ = '\n    A tool target that is a local binary on the system. Can be found using\n    environmentmodules or a path on the executing machine. A local binary\n    target has a number of fields that can be supplied:\n\n    * ``binary (required)``: the name of the binary/script to call, can also be called ``bin``\n      for backwards compatibility.\n    * ``modules``: list of modules to load, this can be environmentmodules or lmod\n      modules. If modules are given, the ``paths``, ``environment_variables`` and ``initscripts``\n      are ignored.\n    * ``paths``: a list of paths to add following the structure ``{"value": "/path/to/dir", "type": "bin"}``.\n      The types can be ``bin`` if the it should be added to $PATH or ``lib`` if it should be\n      added to te library path (e.g. $LD_LIBRARY_PATH for linux).\n    * ``environment_variables``: a dictionary of environment variables to set.\n    * ``initscript``: a list of script to run before running the main tool\n    * ``interpreter``: the interpreter to use to call the binary e.g. ``python``\n\n    The LocalBinaryTarget will first check if there are modules given and the module subsystem is loaded.\n    If that is the case it will simply unload all current modules and load the given modules. If not it\n    will try to set up the environment itself by using the following steps:\n\n    1. Prepend the bin paths to $PATH\n    2. Prepend the lib paths to the correct environment variable\n    3. Setting the other environment variables given ($PATH and the system\n       library path are ignored and cannot be set that way)\n    4. Call the initscripts one by one\n\n    The definition of the target in JSON is very straightforward:\n\n    .. code-block:: json\n\n        {\n          "binary": "bin/test.py",\n          "interpreter": "python",\n          "paths": [\n            {\n              "type": "bin",\n              "value": "vfs://apps/test/bin"\n            },\n            {\n              "type": "lib",\n              "value": "./lib"\n            }\n          ],\n          "environment_variables": {\n            "othervar": 42,\n            "short_var": 1,\n            "testvar": "value1"\n          },\n          "initscripts": [\n            "bin/init.sh"\n          ],\n          "modules": ["elastix/4.8"]\n        }\n\n    In XML the definition would be in the form of:\n\n   .. code-block:: xml\n\n        <target os="linux" arch="*" modules="elastix/4.8" bin="bin/test.py" interpreter="python">\n          <paths>\n            <path type="bin" value="vfs://apps/test/bin" />\n            <path type="lib" value="./lib" />\n          </paths>\n          <environment_variables short_var="1">\n            <testvar>value1</testvar>\n            <othervar>42</othervar>\n          </environment_variables>\n          <initscripts>\n            <initscript>bin/init.sh</initscript>\n          </initscripts>\n        </target>\n    '
    DYNAMIC_LIBRARY_PATH_DICT = {'windows':'PATH', 
     'linux':'LD_LIBRARY_PATH', 
     'darwin':'DYLD_LIBRARY_PATH'}
    _platform = platform.system().lower()
    if _platform not in DYNAMIC_LIBRARY_PATH_DICT:
        fastr.log.warning('"Dynamic library path not supported on platform: {}"'.format(_platform))

    def __init__(self, binary, paths=None, environment_variables=None, initscripts=None, modules=None, interpreter=None, **kwargs):
        """
        Define a new local binary target. Must be defined either using paths and optionally environment_variables
        and initscripts, or enviroment modules.
        """
        self.binary = binary
        if modules is None:
            if 'module' in kwargs:
                if kwargs['module'] is not None:
                    fastr.log.warning('Using deprecated module in target (modules is new way to do it)')
                    self._modules = (kwargs['module'],)
            self._modules = None
        else:
            if isinstance(modules, str):
                self._modules = (
                 modules.strip(),)
            else:
                self._modules = tuple(x.strip() for x in modules)
            if isinstance(paths, str):
                self._paths = [
                 {'type':'bin', 
                  'value':paths}]
            elif paths is None:
                if 'location' in kwargs:
                    if kwargs['location'] is not None:
                        fastr.log.warning('Using deprecated location in target (paths is the new way to do it)')
                        self._paths = [{'type':'bin',  'value':kwargs['location']}]
            else:
                self._paths = paths
        if self._paths is not None:
            for path_entry in self._paths:
                if not url.isurl(path_entry['value']):
                    fastr.log.info('Changing {}'.format(path_entry['value']))
                    path_entry['value'] = os.path.abspath(path_entry['value'])

        if environment_variables is None:
            environment_variables = {}
        self._envvar = environment_variables
        if initscripts is None:
            initscripts = []
        self._init_scripts = [os.path.abspath(x) for x in initscripts]
        self.interpreter = interpreter
        self._roll_back = None

    def __enter__(self):
        super(LocalBinaryTarget, self).__enter__()
        if self._platform in self.DYNAMIC_LIBRARY_PATH_DICT:
            dynamic_library_path = self.DYNAMIC_LIBRARY_PATH_DICT[self._platform]
        else:
            dynamic_library_path = None
        if ENVIRONMENT_MODULES_LOADED:
            if self._modules is not None:
                if len(self._modules) > 0:
                    ENVIRONMENT_MODULES.clear()
                    for module_ in self._modules:
                        if not ENVIRONMENT_MODULES.isloaded(module_):
                            ENVIRONMENT_MODULES.load(module_)
                            fastr.log.info('loaded module: {}'.format(module_))
                        if not ENVIRONMENT_MODULES.isloaded(module_):
                            raise exceptions.FastrImportError('EnvironmentModule {} could not be loaded!'.format(module_))

                    fastr.log.info('LoadedModules: {}'.format(ENVIRONMENT_MODULES.loaded_modules))
        else:
            if self._paths is not None:
                self._roll_back = {'PATH': os.environ.get('PATH', None)}
                bin_path = os.environ.get('PATH', None)
                bin_path = [bin_path] if bin_path else []
                extra_path = [x['value'] for x in self._paths if x['type'] == 'bin']
                extra_path = [fastr.vfs.url_to_path(x) if url.isurl(x) else x for x in extra_path]
                fastr.log.info('Adding extra PATH: {}'.format(extra_path))
                os.environ['PATH'] = os.pathsep.join(extra_path + bin_path)
                extra_ld_library_path = [x['value'] for x in self._paths if x['type'] == 'lib']
                if len(extra_ld_library_path) > 0:
                    if dynamic_library_path is None:
                        message = 'Cannot set dynamic library path on platform: {}'.format(self._platform)
                        fastr.log.critical(message)
                        raise exceptions.FastrNotImplementedError(message)
                    self._roll_back[dynamic_library_path] = os.environ.get(dynamic_library_path, None)
                    lib_path = os.environ.get(dynamic_library_path, None)
                    lib_path = [lib_path] if lib_path else []
                    extra_ld_library_path = [fastr.vfs.url_to_path(x) if url.isurl(x) else x for x in extra_ld_library_path]
                    fastr.log.info('Adding extra LIB: {}'.format(extra_ld_library_path))
                    os.environ[dynamic_library_path] = os.pathsep.join(extra_ld_library_path + lib_path)
                for var, value in self._envvar.items():
                    if var in ['PATH', dynamic_library_path]:
                        pass
                    else:
                        self._roll_back[var] = os.environ.get(var, None)
                        os.environ = str(value)

                for script in self._init_scripts:
                    if isinstance(script, str):
                        script = [
                         script]
                    subprocess.call(script)

            else:
                raise exceptions.FastrNotImplementedError('Binary targets must have either paths or modules set! (binary {})'.format(self.binary))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Cleanup the environment
        """
        if ENVIRONMENT_MODULES_LOADED:
            if self._modules is not None:
                if len(self._modules) > 0:
                    ENVIRONMENT_MODULES.clear()
        if self._roll_back is not None:
            for var, value in self._roll_back.items():
                if value is not None:
                    os.environ[var] = value
                else:
                    del os.environ[var]

            self._roll_back = None

    def run_command(self, command: List) -> TargetResult:
        if self.interpreter is not None:
            paths = [x['value'] for x in self._paths if x['type'] == 'bin']
            fastr.log.info('Options: {}'.format(paths))
            try:
                containing_path = next(x for x in paths if os.path.exists(os.path.join(x, command[0])))
            except StopIteration:
                raise exceptions.FastrScriptNotFoundError(self.interpreter, command[0], paths)

            interpreter = self.interpreter
            command = [
             interpreter, os.path.join(containing_path, command[0])] + command[1:]
        fastr.log.debug('COMMAND: "{}" ({})'.format(command, type(command).__name__))
        return self.call_subprocess(command)

    @property
    def paths(self):
        return self._paths