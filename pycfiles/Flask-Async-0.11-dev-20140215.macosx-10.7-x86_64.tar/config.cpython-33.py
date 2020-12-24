# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mrdon/dev/flask-async/venv/lib/python3.3/site-packages/flask/config.py
# Compiled at: 2014-02-15 13:00:30
# Size of source mod 2**32: 7337 bytes
"""
    flask.config
    ~~~~~~~~~~~~

    Implements the configuration related objects.

    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import imp, os, errno
from werkzeug.utils import import_string
from ._compat import string_types
from . import json

class ConfigAttribute(object):
    __doc__ = 'Makes an attribute forward to the config'

    def __init__(self, name, get_converter=None):
        self.__name__ = name
        self.get_converter = get_converter

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        else:
            rv = obj.config[self.__name__]
            if self.get_converter is not None:
                rv = self.get_converter(rv)
            return rv

    def __set__(self, obj, value):
        obj.config[self.__name__] = value


class Config(dict):
    __doc__ = "Works exactly like a dict but provides ways to fill it from files\n    or special dictionaries.  There are two common patterns to populate the\n    config.\n\n    Either you can fill the config from a config file::\n\n        app.config.from_pyfile('yourconfig.cfg')\n\n    Or alternatively you can define the configuration options in the\n    module that calls :meth:`from_object` or provide an import path to\n    a module that should be loaded.  It is also possible to tell it to\n    use the same module and with that provide the configuration values\n    just before the call::\n\n        DEBUG = True\n        SECRET_KEY = 'development key'\n        app.config.from_object(__name__)\n\n    In both cases (loading from any Python file or loading from modules),\n    only uppercase keys are added to the config.  This makes it possible to use\n    lowercase values in the config file for temporary values that are not added\n    to the config or to define the config keys in the same file that implements\n    the application.\n\n    Probably the most interesting way to load configurations is from an\n    environment variable pointing to a file::\n\n        app.config.from_envvar('YOURAPPLICATION_SETTINGS')\n\n    In this case before launching the application you have to set this\n    environment variable to the file you want to use.  On Linux and OS X\n    use the export statement::\n\n        export YOURAPPLICATION_SETTINGS='/path/to/config/file'\n\n    On windows use `set` instead.\n\n    :param root_path: path to which files are read relative from.  When the\n                      config object is created by the application, this is\n                      the application's :attr:`~flask.Flask.root_path`.\n    :param defaults: an optional dictionary of default values\n    "

    def __init__(self, root_path, defaults=None):
        dict.__init__(self, defaults or {})
        self.root_path = root_path

    def from_envvar(self, variable_name, silent=False):
        """Loads a configuration from an environment variable pointing to
        a configuration file.  This is basically just a shortcut with nicer
        error messages for this line of code::

            app.config.from_pyfile(os.environ['YOURAPPLICATION_SETTINGS'])

        :param variable_name: name of the environment variable
        :param silent: set to `True` if you want silent failure for missing
                       files.
        :return: bool. `True` if able to load config, `False` otherwise.
        """
        rv = os.environ.get(variable_name)
        if not rv:
            if silent:
                return False
            raise RuntimeError('The environment variable %r is not set and as such configuration could not be loaded.  Set this variable and make it point to a configuration file' % variable_name)
        return self.from_pyfile(rv, silent=silent)

    def from_pyfile(self, filename, silent=False):
        """Updates the values in the config from a Python file.  This function
        behaves as if the file was imported as module with the
        :meth:`from_object` function.

        :param filename: the filename of the config.  This can either be an
                         absolute filename or a filename relative to the
                         root path.
        :param silent: set to `True` if you want silent failure for missing
                       files.

        .. versionadded:: 0.7
           `silent` parameter.
        """
        filename = os.path.join(self.root_path, filename)
        d = imp.new_module('config')
        d.__file__ = filename
        try:
            with open(filename) as (config_file):
                exec(compile(config_file.read(), filename, 'exec'), d.__dict__)
        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise

        self.from_object(d)
        return True

    def from_object(self, obj):
        """Updates the values from the given object.  An object can be of one
        of the following two types:

        -   a string: in this case the object with that name will be imported
        -   an actual object reference: that object is used directly

        Objects are usually either modules or classes.

        Just the uppercase variables in that object are stored in the config.
        Example usage::

            app.config.from_object('yourapplication.default_config')
            from yourapplication import default_config
            app.config.from_object(default_config)

        You should not use this function to load the actual configuration but
        rather configuration defaults.  The actual config should be loaded
        with :meth:`from_pyfile` and ideally from a location not within the
        package because the package might be installed system wide.

        :param obj: an import name or object
        """
        if isinstance(obj, string_types):
            obj = import_string(obj)
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)
                continue

    def from_json(self, filename, silent=False):
        """Updates the values in the config from a JSON file. This function
        behaves as if the JSON object was a dictionary and passed ot the
        :meth:`from_object` function.

        :param filename: the filename of the JSON file.  This can either be an
                         absolute filename or a filename relative to the
                         root path.
        :param silent: set to `True` if you want silent failure for missing
                       files.

        .. versionadded:: 1.0
        """
        filename = os.path.join(self.root_path, filename)
        try:
            with open(filename) as (json_file):
                obj = json.loads(json_file.read())
        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise

        for key in obj.keys():
            if key.isupper():
                self[key] = obj[key]
                continue

        return True

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, dict.__repr__(self))