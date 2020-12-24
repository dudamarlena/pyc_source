# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/file_parsers/json_parser.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 6660 bytes
import logging
logger = logging.getLogger(__name__)
from distutils.version import LooseVersion
import json, zipfile, os, io
from shutil import move
from pyxrd.__version import __version__
from pyxrd.file_parsers.base_parser import BaseParser
from pyxrd.generic.io.json_codec import PyXRDDecoder, PyXRDEncoder
from pyxrd.generic.io.custom_io import storables, COMPRESSION
from pyxrd.generic.io.utils import unicode_open

class JSONParser(BaseParser):
    __doc__ = '\n        PyXRD Object JSON Parser\n    '
    description = 'PyXRD Object JSON'
    mimetypes = ['application/octet-stream', 'application/zip']
    __file_mode__ = 'r'

    @classmethod
    def _get_file(cls, fp, close=None):
        """
            Returns a three-tuple:
            filename, zipfile-object, close
        """
        if isinstance(fp, str):
            filename = fp
            if zipfile.is_zipfile(filename):
                fp = zipfile.ZipFile(filename, cls.__file_mode__)
            else:
                fp = unicode_open(filename, cls.__file_mode__)
            close = True if close is None else close
        else:
            filename = getattr(fp, 'name', None)
            if zipfile.is_zipfile(fp):
                fp = zipfile.ZipFile(fp)
            close = False if close is None else close
        return (
         filename, fp, close)

    @classmethod
    def _parse_header(cls, filename, fp, data_objects=None, close=False):
        return data_objects

    @classmethod
    def _parse_data(cls, filename, fp, data_objects=None, close=True):
        is_zipfile = isinstance(fp, zipfile.ZipFile)
        if is_zipfile:
            namelist = fp.namelist()
            if 'content' in namelist:
                obj = None
                decoder = json.JSONDecoder()

                def get_named_item(fpt, name):
                    try:
                        cf = fpt.open(name, cls.__file_mode__)
                        obj = decoder.decode(cf.read().decode('utf-8'))
                    finally:
                        cf.close()

                    return obj

                obj = get_named_item(fp, 'content')
                if 'version' in namelist:
                    namelist.remove('version')
                    version = get_named_item(fp, 'version')
                    if LooseVersion(version) > LooseVersion(__version__.replace('v', '')):
                        raise RuntimeError('Unsupported project' + "version '%s', program version is '%s'" % (
                         version, __version__))
                else:
                    logging.warn('Loading pre-v0.8 file format, might be deprecated!')
                if not hasattr(obj, 'update'):
                    raise RuntimeError('Decoding a multi-part JSON object requires the root to be a dictionary object!')
                for sub_name in namelist:
                    if sub_name != 'content':
                        obj['properties'][sub_name] = get_named_item(fp, sub_name)

                data_objects = PyXRDDecoder(mapper=storables).__pyxrd_decode__(obj) or obj
            else:
                data_objects = []
                for sub_name in namelist:
                    zpf = fp.open(sub_name, cls.__file_mode__)
                    data_objects.append(cls.parse(zpf))
                    zpf.close()

        else:
            if hasattr(fp, 'seek'):
                try:
                    fp.seek(0)
                except io.UnsupportedOperation:
                    pass

                data_objects = PyXRDDecoder.decode_file(fp, mapper=storables)
            if close:
                fp.close()
            return data_objects

    @staticmethod
    def write(obj, file, zipped=False):
        """
        Saves the output from dump_object() to `filename`, optionally zipping it.
        File can be either a filename or a file-like object. If it is a filename
        extra precautions are taken to prevent malformed data overwriting a good
        file. With file objects this is not the case.
        """
        filename = None
        if isinstance(file, str):
            filename = file
            file = filename + '.tmp'
            backup_name = filename + '~'
        try:
            if zipped:
                with zipfile.ZipFile(file, mode='w', compression=COMPRESSION) as (f):
                    for partname, json_object in obj.to_json_multi_part():
                        f.writestr(partname, PyXRDEncoder.dump_object(json_object))

            elif filename is not None:
                with unicode_open(file, 'w') as (f):
                    PyXRDEncoder.dump_object_to_file(obj, f)
            else:
                PyXRDEncoder.dump_object_to_file(obj, file)
        except:
            if filename is not None:
                if os.path.exists(file):
                    os.remove(file)
            raise

        if filename is not None:
            if os.path.exists(filename):
                move(filename, backup_name)
            move(file, filename)