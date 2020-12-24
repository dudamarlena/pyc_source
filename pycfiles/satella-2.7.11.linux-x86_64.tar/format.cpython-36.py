# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/configuration/sources/format.py
# Compiled at: 2020-04-22 08:35:40
# Size of source mod 2**32: 2520 bytes
import binascii, codecs, json, typing as tb
from satella.coding.recast_exceptions import rethrow_as
from satella.exceptions import ConfigurationError
from .base import BaseSource
__all__ = [
 'FormatSource', 'FORMAT_SOURCES']
FORMAT_SOURCES = []

def register_format_source(source):
    source_name = source.__name__
    __all__.append(source_name)
    FORMAT_SOURCES.append(source_name)
    return source


def _override_me(key):
    raise NotImplementedError('override me')


class FormatSource(BaseSource):
    __slots__ = ('root', 'encoding')
    TRANSFORM = _override_me
    BASE_EXCEPTIONS = [TypeError, UnicodeDecodeError, ValueError,
     binascii.Error, LookupError]
    EXTRA_EXCEPTIONS = []

    def __init__(self, root, encoding='utf-8'):
        """
        :param root: content
        :type root: if bytes, will be decoded with given encoding'
        """
        super().__init__()
        self.root = root
        self.encoding = encoding

    def provide(self) -> dict:
        cls = self.__class__
        with rethrow_as(tuple(cls.BASE_EXCEPTIONS + cls.EXTRA_EXCEPTIONS), ConfigurationError):
            if isinstance(self.root, bytes):
                self.root = codecs.decode(self.root, self.encoding)
                if isinstance(self.root, bytes):
                    self.root = self.root.decode('utf-8')
                ret_val = cls.TRANSFORM(self.root)
                raise isinstance(ret_val, dict) or ConfigurationError('provider was unable to generate a text volume')
            else:
                return ret_val


@register_format_source
class JSONSource(FormatSource):
    __doc__ = '\n    Loads JSON strings\n    '
    TRANSFORM = json.loads
    EXTRA_EXCEPTIONS = [json.JSONDecodeError]


try:
    import yaml
except ImportError:
    pass
else:

    @register_format_source
    class YAMLSource(FormatSource):
        __doc__ = '\n        Loads YAML strings\n        '
        EXTRA_EXCEPTIONS = [yaml.YAMLError]
        TRANSFORM = lambda data: yaml.load(data, Loader=(yaml.Loader))


try:
    import toml
except ImportError:
    pass
else:

    @register_format_source
    class TOMLSource(FormatSource):
        __doc__ = '\n        Loads TOML strings\n        '
        EXTRA_EXCEPTIONS = [toml.TomlDecodeError]
        TRANSFORM = toml.loads