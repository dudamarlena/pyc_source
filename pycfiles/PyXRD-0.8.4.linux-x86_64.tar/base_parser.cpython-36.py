# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/file_parsers/base_parser.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 5790 bytes
from .meta_parser import MetaParser
from .data_object import DataObject
import types

class BaseParser(object, metaclass=MetaParser):
    __doc__ = '\n        Base class providing some common attributes and functions.\n        Do not register this class or subclasses without overriding the\n        following functions:\n            - parse_header\n            - parse_data\n            - parse (optional)\n            - setup_file_filter (optional)\n    '
    description = 'Base Parser'
    extensions = []
    mimetypes = []

    @property
    def can_write(self):
        return getattr(self, 'write', None) is not None

    @property
    def can_read(self):
        return getattr(self, 'parse', None) is not None

    data_object_type = DataObject
    __file_mode__ = 'r'
    file_filter = None

    @classmethod
    def _get_file(cls, fp, close=None):
        """
            Returns a three-tuple:
            filename, file-object, close
        """
        if isinstance(fp, str):
            return (fp, open(fp, cls.__file_mode__), True if close is None else close)
        else:
            return (
             getattr(fp, 'name', None), fp, False if close is None else close)

    @classmethod
    def _adapt_data_object_list(cls, data_objects, num_samples, only_extend=False):
        if data_objects == None:
            data_objects = [
             None]
        else:
            num_data_objects = len(data_objects)
            if num_data_objects < num_samples:
                data_objects.extend([None] * int(num_samples - num_data_objects))
            if not only_extend:
                if num_data_objects > num_samples:
                    data_objects = data_objects[:num_samples]
        for i in range(num_samples):
            if not data_objects[i]:
                data_objects[i] = cls.data_object_type()

        return data_objects

    @classmethod
    def _parse_header(cls, filename, fp, data_objects=None, close=False):
        """
            This method is implemented by sub-classes.
            It should parse the file and returns a list of DataObjects 
            with the header properties filled in accordingly.
            The filename argument is always required. If no file object is passed
            as keyword argument, it only serves as a label. Otherwise a new file
            object is created. 
            File objects are not closed unless close is set to True.
            Existing DataObjects can be passed as well and will then 
            be used instead of creating new ones.
        """
        raise NotImplementedError

    @classmethod
    def _parse_data(cls, filename, fp, data_objects=None, close=False):
        """
            This method is implemented by sub-classes.
            It should parse the file and return a list of DataObjects
            with the data properties filled in accordingly.
            The filename argument is always required. If no file object is passed
            as keyword argument, it only serves as a label. Otherwise a new file
            object is created.
            File objects are not closed unless close is set to True.
            Existing DataObjects can be passed as well and will then 
            be used instead of creating new ones.
        """
        raise NotImplementedError

    @classmethod
    def parse(cls, fp, data_objects=None, close=True):
        """
            This method parses the file and return a list of DataObjects
            with both header and data properties filled in accordingly.
            The filename argument is always required. If no file object is passed
            as keyword argument, it only serves as a label. Otherwise a new file
            object is created.
            File objects are closed unless close is set to False.
            Existing DataObjects can be passed as well and will then 
            be used instead of creating new ones.
        """
        filename, fp, close = cls._get_file(fp, close=close)
        data_objects = cls._parse_header(filename, fp, data_objects=data_objects)
        data_objects = cls._parse_data(filename, fp, data_objects=data_objects)
        if close:
            fp.close()
        return data_objects

    @classmethod
    def setup_file_filter(cls):
        """
            Creates a file filter based on a list of extensions set in the
            'extensions' attribute of the class using the 'description' attribute
            as the name for the filter. If the 'mimetypes' attribute is also set,
            it will also set these. If additional properties are needed, this function
            should be overriden by subclasses.
        """
        if cls.file_filter == None:
            if cls.description != '':
                if cls.extensions:
                    try:
                        import gi
                        gi.require_version('Gtk', '3.0')
                        from gi.repository import Gtk
                    except ImportError:
                        pass
                    else:
                        cls.file_filter = Gtk.FileFilter()
                        cls.file_filter.set_name(cls.description)
                        for mtpe in cls.mimetypes:
                            pass

                        for expr in cls.extensions:
                            cls.file_filter.add_pattern(expr)

                        setattr(cls.file_filter, 'parser', cls)