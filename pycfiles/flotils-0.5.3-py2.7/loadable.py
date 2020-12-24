# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\flotils\loadable.py
# Compiled at: 2019-04-14 18:27:11
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
__author__ = b'the01'
__email__ = b'jungflor@gmail.com'
__copyright__ = b'Copyright (C) 2013-19, Florian JUNG'
__license__ = b'MIT'
__version__ = b'0.4.1'
__date__ = b'2019-04-14'
import os, datetime, json, io, sys, yaml
from .logable import Logable, ModuleLogable

class Logger(ModuleLogable):
    pass


logger = Logger()

class DateTimeEncoder(json.JSONEncoder):
    """ Encode datetime, date and time objects for json """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            if obj.tzinfo:
                obj = (obj - obj.tzinfo.utcoffset(obj)).replace(tzinfo=None)
            return {b'__datetime__': obj.isoformat() + b'Z'}
        else:
            if isinstance(obj, datetime.date):
                return {b'__date__': obj.isoformat()}
            if isinstance(obj, datetime.timedelta):
                return {b'__type__': b'timedelta', 
                   b'days': obj.days, 
                   b'seconds': obj.seconds, 
                   b'microseconds': obj.microseconds}
            if isinstance(obj, datetime.time):
                return {b'__time__': obj.isoformat()}
            return super(DateTimeEncoder, self).default(obj)


class DateTimeDecoder(object):
    """ Decode datetime, date and time from json """

    @staticmethod
    def _as_datetime(dct):
        if b'__datetime__' in dct.keys():
            try:
                return datetime.datetime.strptime(dct[b'__datetime__'], b'%Y-%m-%dT%H:%M:%S.%fZ')
            except ValueError:
                return datetime.datetime.strptime(dct[b'__datetime__'], b'%Y-%m-%dT%H:%M:%SZ')

        raise TypeError(b'Not Datetime')

    @staticmethod
    def _as_date(dct):
        if b'__date__' in dct:
            d = datetime.datetime.strptime(dct[b'__date__'], b'%Y-%m-%d')
            if d:
                return d.date()
            return d
        raise TypeError(b'Not Date')

    @staticmethod
    def _as_time(dct):
        if b'__time__' in dct:
            try:
                d = datetime.datetime.strptime(dct[b'__time__'], b'%H:%M:%S.%f')
            except ValueError:
                d = datetime.datetime.strptime(dct[b'__time__'], b'%H:%M:%S')

            if d:
                return d.time()
            return d
        raise TypeError(b'Not Time')

    @staticmethod
    def decode(dct):
        if not isinstance(dct, dict):
            return dct
        if b'__type__' in dct:
            obj_type = dct.pop(b'__type__')
            if obj_type == b'timedelta':
                return datetime.timedelta(**dct)
            dct[b'__type__'] = obj_type
        try:
            return DateTimeDecoder._as_datetime(dct)
        except:
            try:
                return DateTimeDecoder._as_date(dct)
            except:
                try:
                    return DateTimeDecoder._as_time(dct)
                except:
                    return dct


def load_json(json_data, decoder=None):
    """
    Load data from json string

    :param json_data: Stringified json object
    :type json_data: str | unicode
    :param decoder: Use custom json decoder
    :type decoder: T <= DateTimeDecoder
    :return: Json data
    :rtype: None | int | float | str | list | dict
    """
    if decoder is None:
        decoder = DateTimeDecoder
    return json.loads(json_data, object_hook=decoder.decode)


def load_json_file(file, decoder=None):
    """
    Load data from json file

    :param file: Readable object or path to file
    :type file: FileIO | str
    :param decoder: Use custom json decoder
    :type decoder: T <= DateTimeDecoder
    :return: Json data
    :rtype: None | int | float | str | list | dict
    """
    if decoder is None:
        decoder = DateTimeDecoder
    if not hasattr(file, b'read'):
        with io.open(file, b'r', encoding=b'utf-8') as (f):
            return json.load(f, object_hook=decoder.decode)
    return json.load(file, object_hook=decoder.decode)


def save_json(val, pretty=False, sort=True, encoder=None):
    """
    Save data to json string

    :param val: Value or struct to save
    :type val: None | int | float | str | list | dict
    :param pretty: Format data to be readable (default: False)
                    otherwise going to be compact
    :type pretty: bool
    :param sort: Sort keys (default: True)
    :type sort: bool
    :param encoder: Use custom json encoder
    :type encoder: T <= DateTimeEncoder
    :return: The jsonified string
    :rtype: str | unicode
    """
    if encoder is None:
        encoder = DateTimeEncoder
    if pretty:
        data = json.dumps(val, indent=4, separators=(',', ': '), sort_keys=sort, cls=encoder)
    else:
        data = json.dumps(val, separators=(',', ':'), sort_keys=sort, cls=encoder)
    if not sys.version_info > (3, 0) and isinstance(data, str):
        data = data.decode(b'utf-8')
    return data


def save_json_file(file, val, pretty=False, compact=True, sort=True, encoder=None):
    """
    Save data to json file

    :param file: Writable object or path to file
    :type file: FileIO | str | unicode
    :param val: Value or struct to save
    :type val: None | int | float | str | list | dict
    :param pretty: Format data to be readable (default: False)
    :type pretty: bool
    :param compact: Format data to be compact (default: True)
    :type compact: bool
    :param sort: Sort keys (default: True)
    :type sort: bool
    :param encoder: Use custom json encoder
    :type encoder: T <= DateTimeEncoder
    :rtype: None
    """
    if encoder is None:
        encoder = DateTimeEncoder
    opened = False
    if not hasattr(file, b'write'):
        file = io.open(file, b'w', encoding=b'utf-8')
        opened = True
    try:
        if pretty:
            data = json.dumps(val, indent=4, separators=(',', ': '), sort_keys=sort, cls=encoder)
        elif compact:
            data = json.dumps(val, separators=(',', ':'), sort_keys=sort, cls=encoder)
        else:
            data = json.dumps(val, sort_keys=sort, cls=encoder)
        if not sys.version_info > (3, 0) and isinstance(data, str):
            data = data.decode(b'utf-8')
        file.write(data)
    finally:
        if opened:
            file.close()

    return


def load_yaml(data):
    """
    Load data from yaml string

    :param data: Stringified yaml object
    :type data: str | unicode
    :return: Yaml data
    :rtype: None | int | float | str | unicode | list | dict
    """
    return yaml.load(data, yaml.FullLoader)


def load_yaml_file(file):
    """
    Load data from yaml file

    :param file: Readable object or path to file
    :type file: FileIO | str | unicode
    :return: Yaml data
    :rtype: None | int | float | str | unicode | list | dict
    """
    if not hasattr(file, b'read'):
        with io.open(file, b'r', encoding=b'utf-8') as (f):
            return yaml.load(f, yaml.FullLoader)
    return yaml.load(file, yaml.FullLoader)


def save_yaml(val):
    """
    Save data to yaml string

    :param val: Value or struct to save
    :type val: None | int | float | str | unicode | list | dict
    :return: The yamlified string
    :rtype: str | unicode
    """
    return yaml.dump(val)


def save_yaml_file(file, val):
    """
    Save data to yaml file

    :param file: Writable object or path to file
    :type file: FileIO | str | unicode
    :param val: Value or struct to save
    :type val: None | int | float | str | unicode | list | dict
    """
    opened = False
    if not hasattr(file, b'write'):
        file = io.open(file, b'w', encoding=b'utf-8')
        opened = True
    try:
        yaml.dump(val, file)
    finally:
        if opened:
            file.close()


def load_file(path):
    """
    Load file

    :param path: Path to file
    :type path: str | unicode
    :return: Loaded data
    :rtype: None | int | float | str | unicode | list | dict
    :raises IOError: If file not found or error accessing file
    """
    res = {}
    if not path:
        IOError(b'No path specified to save')
    if not os.path.isfile(path):
        raise IOError((b'File not found {}').format(path))
    try:
        with io.open(path, b'r', encoding=b'utf-8') as (f):
            if path.endswith(b'.json'):
                res = load_json_file(f)
            elif path.endswith(b'.yaml') or path.endswith(b'.yml'):
                res = load_yaml_file(f)
    except IOError:
        raise
    except Exception as e:
        raise IOError(e)

    return res


def save_file(path, data, readable=False):
    """
    Save to file

    :param path: File path to save
    :type path: str | unicode
    :param data: Data to save
    :type data: None | int | float | str | unicode | list | dict
    :param readable: Format file to be human readable (default: False)
    :type readable: bool
    :rtype: None
    :raises IOError: If empty path or error writing file
    """
    if not path:
        IOError(b'No path specified to save')
    try:
        with io.open(path, b'w', encoding=b'utf-8') as (f):
            if path.endswith(b'.json'):
                save_json_file(f, data, pretty=readable, compact=not readable, sort=True)
            elif path.endswith(b'.yaml') or path.endswith(b'.yml'):
                save_yaml_file(f, data)
    except IOError:
        raise
    except Exception as e:
        raise IOError(e)


def join_path_prefix(path, pre_path=None):
    """
    If path set and not absolute, append it to pre path (if used)

    :param path: path to append
    :type path: str | None
    :param pre_path: Base path to append to (default: None)
    :type pre_path: None |\xa0str
    :return: Path or appended path
    :rtype: str | None
    """
    if not path:
        return path
    if pre_path and not os.path.isabs(path):
        return os.path.join(pre_path, path)
    return path


class Loadable(Logable):
    """
    Class to facilitate loading config from json-files and ease relative paths
    """

    def __init__(self, settings=None):
        """
        Initialize object

        :param settings: Settings for instance (default: None)
        :type settings: dict | None
        :rtype: None
        :raises IOError: Failed to load settings file
        """
        if settings is None:
            settings = {}
        super(Loadable, self).__init__(settings)
        sett_path = settings.get(b'settings_file', None)
        self._pre_path = settings.get(b'path_prefix', None)
        if sett_path:
            sett_path = self.join_path_prefix(sett_path)
            sett = self.load_settings(sett_path)
            sett_prepath = sett.get(b'path_prefix')
            if sett_prepath:
                self._pre_path = self.join_path_prefix(sett_prepath)
            sett.update(settings)
            settings.update(sett)
            self.debug((b'Loaded config {}').format(sett_path))
            super(Loadable, self).__init__(settings)
        return

    @property
    def _prePath(self):
        import warnings
        warnings.warn(b'This variable is no longer in use - Please use _pre_path instead', DeprecationWarning)
        return self._pre_path

    @_prePath.setter
    def set_prePath(self, value):
        import warnings
        warnings.warn(b'This variable is no longer in use - Please use _pre_path instead', DeprecationWarning)
        self._pre_path = value

    def join_path_prefix(self, path):
        """
        If path set and not absolute, append it to self._pre_path

        :param path: Path to append
        :type path: str | None
        :return: Path or appended path
        :rtype: str | None
        """
        return join_path_prefix(path, self._pre_path)

    def _load_json_file(self, file, decoder=None):
        """
        Load data from json file

        :param file: Readable file or path to file
        :type file: FileIO | str | unicode
        :param decoder: Use custom json decoder
        :type decoder: T <= flotils.loadable.DateTimeDecoder
        :return: Json data
        :rtype: None | int | float | str | list | dict
        :raises IOError: Failed to load
        """
        try:
            res = load_json_file(file, decoder=decoder)
        except ValueError as e:
            if (b'{}').format(e) == b'No JSON object could be decoded':
                raise IOError(b'Decoding JSON failed')
            self.exception((b'Failed to load from {}').format(file))
            raise IOError(b'Loading file failed')
        except:
            self.exception((b'Failed to load from {}').format(file))
            raise IOError(b'Loading file failed')

        return res

    def _save_json_file(self, file, val, pretty=False, compact=True, sort=True, encoder=None):
        """
        Save data to json file

        :param file: Writable file or path to file
        :type file: FileIO | str | unicode
        :param val: Value or struct to save
        :type val: None | int | float | str | list | dict
        :param pretty: Format data to be readable (default: False)
        :type pretty: bool
        :param compact: Format data to be compact (default: True)
        :type compact: bool
        :param sort: Sort keys (default: True)
        :type sort: bool
        :param encoder: Use custom json encoder
        :type encoder: T <= flotils.loadable.DateTimeEncoder
        :rtype: None
        :raises IOError: Failed to save
        """
        try:
            save_json_file(file, val, pretty, compact, sort, encoder)
        except:
            self.exception((b'Failed to save to {}').format(file))
            raise IOError(b'Saving file failed')

    def _load_yaml_file(self, file):
        """
        Load data from yaml file

        :param file: Readable object or path to file
        :type file: FileIO | str | unicode
        :return: Yaml data
        :rtype: None | int | float | str | unicode | list | dict
        :raises IOError: Failed to load
        """
        try:
            res = load_yaml_file(file)
        except:
            self.exception((b'Failed to load from {}').format(file))
            raise IOError(b'Loading file failed')

        return res

    def _save_yaml_file(self, file, val):
        """
        Save data to yaml file

        :param file: Writable object or path to file
        :type file: FileIO | str | unicode
        :param val: Value or struct to save
        :type val: None | int | float | str | unicode | list | dict
        :raises IOError: Failed to save
        """
        try:
            save_yaml_file(file, val)
        except:
            self.exception((b'Failed to save to {}').format(file))
            raise IOError(b'Saving file failed')

    def load_settings(self, path):
        """
        Load settings dict

        :param path: Path to settings file
        :type path: str | unicode
        :return: Loaded settings
        :rtype: dict
        :raises IOError: If file not found or error accessing file
        :raises TypeError: Settings file does not contain dict
        """
        res = self.load_file(path)
        if not isinstance(res, dict):
            raise TypeError(b'Expected settings to be dict')
        return res

    def save_settings(self, path, settings, readable=False):
        """
        Save settings to file

        :param path: File path to save
        :type path: str | unicode
        :param settings: Settings to save
        :type settings: dict
        :param readable: Format file to be human readable (default: False)
        :type readable: bool
        :rtype: None
        :raises IOError: If empty path or error writing file
        :raises TypeError: Settings is not a dict
        """
        if not isinstance(settings, dict):
            raise TypeError(b'Expected settings to be dict')
        return self.save_file(path, settings, readable)

    def load_file(self, path):
        """
        Load file

        :param path: Path to file
        :type path: str | unicode
        :return: Loaded settings
        :rtype: None | str | unicode | int | list | dict
        :raises IOError: If file not found or error accessing file
        """
        res = None
        if not path:
            IOError(b'No path specified to save')
        if not os.path.isfile(path):
            raise IOError((b'File not found {}').format(path))
        try:
            with io.open(path, b'r', encoding=b'utf-8') as (f):
                if path.endswith(b'.json'):
                    res = self._load_json_file(f)
                elif path.endswith(b'.yaml') or path.endswith(b'.yml'):
                    res = self._load_yaml_file(f)
        except IOError:
            raise
        except Exception as e:
            self.exception((b'Failed reading {}').format(path))
            raise IOError(e)

        return res

    def save_file(self, path, data, readable=False):
        """
        Save to file

        :param path: File path to save
        :type path: str | unicode
        :param data: To save
        :type data: None | str | unicode | int | list | dict
        :param readable: Format file to be human readable (default: False)
        :type readable: bool
        :rtype: None
        :raises IOError: If empty path or error writing file
        """
        if not path:
            IOError(b'No path specified to save')
        try:
            with io.open(path, b'w', encoding=b'utf-8') as (f):
                if path.endswith(b'.json'):
                    self._save_json_file(f, data, pretty=readable, compact=not readable, sort=True)
                elif path.endswith(b'.yaml') or path.endswith(b'.yml'):
                    self._save_yaml_file(f, data)
        except IOError:
            raise
        except Exception as e:
            self.exception((b'Failed writing {}').format(path))
            raise IOError(e)