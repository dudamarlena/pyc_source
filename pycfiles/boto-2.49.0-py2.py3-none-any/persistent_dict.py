# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/persistent_dict.py
# Compiled at: 2012-08-16 08:17:49
__doc__ = '\nPersistent Dictionary Class\n\nProvides persistent dictionary support. Loads the full file into memory, leaves \nit there for full speed dict access, and then writes the full dict back on \nclose (with an atomic commit).\n\nUseful when lookup and mutation speed are more important than the time spent on \nthe initial load and the final write-back.\n\nSimilar to the "F" mode in the gdbm module: "The F flag opens the database in \nfast mode. Writes to the database will not be flushed".\n\n'
import pickle, marshal, ujson as json, csv, os, shutil, ordereddict, bidict, numpy
from botnee import debug
import logging
LOADERS = (
 marshal.loads,
 json.loads,
 pickle.loads,
 csv.reader)

class PersistentDict(ordereddict.OrderedDict):
    """ Persistent dictionary with an API compatible with shelve and anydbm.
    
    The dict is kept in memory, so the dictionary operations run as fast as
    a regular dictionary.
    
    Write to disk is delayed until close or flush (similar to gdbm's fast mode).
    
    Input file format is automatically discovered.
    Output file format is selectable between pickle, marshal json, and csv.
    All serialization formats are backed by fast C implementations.
    """

    def __init__(self, params, verbose=False, logger=None):
        ordereddict.OrderedDict.__init__(self)
        self.flag = params['flag']
        self.mode = params['mode']
        self.format = params['format']
        self.filename = params['filename']
        self.persistent = params['persistent']
        if 'ignore_on_load' in params:
            self.ignore_on_load = params['ignore_on_load']
        else:
            self.ignore_on_load = []
        if self.persistent and self.flag != 'n' and os.access(self.filename, os.R_OK):
            mode = 'rb' if self.format in ('pickle', 'marshal') else 'r'
            fileobj = open(self.filename, mode)
            with fileobj:
                self.load(fileobj, verbose, logger)

    def flush(self, verbose=True, logger=None):
        """Write dict to disk"""
        if not self.persistent:
            return
        else:
            with debug.Timer(self.__module__, None, verbose, logger):
                if self.flag == 'r':
                    return
                filename = self.filename
                tempname = filename + '.tmp'
                mode = 'wb' if self.format in ('pickle', 'marshal') else 'w'
                fileobj = open(tempname, mode)
                try:
                    try:
                        self.dump(fileobj)
                    except Exception:
                        os.remove(tempname)
                        raise

                finally:
                    fileobj.close()

                shutil.move(tempname, self.filename)
                if self.mode is not None:
                    os.chmod(self.filename, self.mode)
            return

    def close(self):
        self.flush()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        if self.persistent:
            self.close()

    def dump(self, fileobj):
        """
        Dumps to disk
        """
        types = {}
        dtypes = {}
        file_dict = {}
        caster = unicode
        for (key, value) in self.items():
            if 'pseudo' in key:
                continue
            if key in self.ignore_on_load:
                continue
            module = value.__class__.__module__
            if module == '__builtin__':
                types[key] = value.__class__.__name__
            else:
                types[key] = module + '.' + value.__class__.__name__
            if type(value) in [numpy.array, numpy.ndarray]:
                try:
                    file_dict[key] = caster(value.tolist())
                except:
                    debug.debug_here()
                else:
                    dtypes[key] = caster(value.dtype)
            elif isinstance(value, numpy.generic):
                file_dict[key] = caster(value)
                dtypes[key] = caster(value.dtype)
            elif type(value) in [ordereddict.OrderedDict, bidict.bidict, dict]:
                file_dict[key] = dict(value)
            elif type(value) in [list, tuple, set, frozenset]:
                file_dict[key] = value
            else:
                file_dict[key] = value
                dtypes[key] = caster(type(value))

        file_dict['types'] = types
        file_dict['dtypes'] = dtypes
        if self.format == 'csv':
            csv.writer(fileobj).writerows(self.items())
        elif self.format == 'json':
            try:
                json.dump(file_dict, fileobj)
            except:
                debug.debug_here()

        elif self.format == 'pickle':
            pickle.dump(dict(self), fileobj, 2)
        elif self.format == 'marshal':
            try:
                marshal.dump(file_dict, fileobj, 2)
            except ValueError, e:
                debug.debug_here()
                raise e

        else:
            raise NotImplementedError('Unknown format: ' + repr(self.format))

    def load(self, fileobj, verbose=False, logger=None):
        with debug.Timer(self.__repr__(), None, verbose, logger):
            for loader in LOADERS:
                msg = 'Loading %s (%s)' % (self.filename, loader.__module__)
                debug.print_verbose(msg, verbose, logger)
                fileobj.seek(0)
                file_dict = {}
                try:
                    s = fileobj.read()
                    debug.print_verbose('File read, calling loader', verbose, logger)
                    file_dict = loader(s)
                    debug.print_verbose('File loaded', verbose, logger)
                    for (key, value) in file_dict['types'].items():
                        skip = False
                        for item in self.ignore_on_load:
                            if key.startswith(item):
                                debug.print_verbose(key + ' ignored', verbose, logger)
                                skip = True
                                break

                        if not skip:
                            self.process_item(file_dict, key, value, verbose, logger)

                    return
                except ValueError:
                    continue

        raise ValueError('File not in a supported format')
        return

    def process_item(self, file_dict, key, value, verbose=False, logger=None):
        """
        Processes a single item from the loaded file
        """
        base = self.__class__
        basecall = super(base, self)
        if key not in ('types', 'dtypes'):
            msg = '(%s, type=<%s>)' % (key, value)
            with debug.Timer(msg, None, verbose, self.logger):
                if value in ('numpy.ndarray', 'numpy.float64'):
                    try:
                        basecall.__setitem__(key, numpy.array(eval(file_dict[key]), dtype=file_dict['dtypes'][key]))
                    except Exception, e:
                        msg = 'Failed to load %s from disk: %s' % (key, e)
                        debug.print_verbose(msg, verbose, logger, logging.WARNING)
                        basecall.__setitem__(key, None)

                else:
                    try:
                        eval('basecall.__setitem__(key, %s(file_dict[key]))' % value)
                    except Exception, e:
                        msg = 'Failed to load %s from disk: %s' % (key, e)
                        debug.print_verbose(msg, verbose, logger, logging.WARNING)
                        basecall.__setitem__(key, None)

        return