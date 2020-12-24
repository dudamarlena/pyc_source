# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nearl/projects/specutils/build/lib/specutils/io/registers.py
# Compiled at: 2020-01-06 12:55:36
# Size of source mod 2**32: 6201 bytes
"""
A module containing the mechanics of the specutils io registry.
"""
import os, logging
from functools import wraps
import astropy.io as io_registry
from ..spectra import Spectrum1D, SpectrumList
__all__ = [
 'data_loader', 'custom_writer', 'get_loaders_by_extension']

def data_loader(label, identifier=None, dtype=Spectrum1D, extensions=None, priority=0):
    """
    Wraps a function that can be added to an `~astropy.io.registry` for custom
    file reading.

    Parameters
    ----------
    label : str
        The label given to the function inside the registry.
    identifier : func
        The identified function used to verify that a file is to use a
        particular file.
    dtype : class
        A class reference for which the data loader should be store.
    extensions : list
        A list of file extensions this loader supports loading from. In the
        case that no identifier function is defined, but a list of file
        extensions is, a simple identifier function will be created to check
        for consistency with the extensions.
    priority : int
        Set the priority of the loader. Currently influences the sorting of the
        returned loaders for a dtype.
    """

    def identifier_wrapper(ident):

        def wrapper(*args, **kwargs):
            try:
                return ident(*args, **kwargs)
            except Exception as e:
                try:
                    logging.debug('Tried to read this as {} file, but could not.'.format(label))
                    logging.debug(e, exc_info=True)
                    return False
                finally:
                    e = None
                    del e

        return wrapper

    def decorator(func):
        io_registry.register_reader(label, dtype, func)
        if identifier is None:
            if extensions is not None:
                logging.info("'{}' data loader provided for {} without explicit identifier. Creating identifier using list of compatible extensions".format(label, dtype.__name__))
                id_func = lambda *args, **kwargs: any([args[1].endswith(x) for x in extensions])
            else:
                logging.warning("'{}' data loader provided for {} without explicit identifier or list of compatible extensions".format(label, dtype.__name__))
                id_func = lambda *args, **kwargs: True
        else:
            id_func = identifier_wrapper(identifier)
        io_registry.register_identifier(label, dtype, id_func)
        func.extensions = extensions
        func.priority = priority
        sorted_loaders = sorted((io_registry._readers.items()), key=(lambda item: getattr(item[1], 'priority', 0)))
        io_registry._readers.clear()
        io_registry._readers.update(sorted_loaders)
        logging.debug('Successfully loaded reader "{}".'.format(label))
        if dtype is Spectrum1D:

            def load_spectrum_list(*args, **kwargs):
                return SpectrumList([func(*args, **kwargs)])

            load_spectrum_list.extensions = extensions
            load_spectrum_list.priority = priority
            io_registry.register_reader(label, SpectrumList, load_spectrum_list)
            io_registry.register_identifier(label, SpectrumList, id_func)
            logging.debug('Created SpectrumList reader for "{}".'.format(label))

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


def custom_writer(label, dtype=Spectrum1D):

    def decorator(func):
        io_registry.register_writer(label, Spectrum1D, func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


def get_loaders_by_extension(extension):
    """
    Retrieve a list of loader labels associated with a given extension.

    Parameters
    ----------
    extension : str
        The extension for which associated loaders will be matched against.

    Returns
    -------
    loaders : list
        A list of loader names that are associated with the extension.
    """
    return [fmt for (fmt, cls), func in io_registry._readers.items() if issubclass(cls, Spectrum1D) if func.extensions is not None if extension in func.extensions]


def _load_user_io():
    path = os.path.expanduser('~/.specutils')
    if not os.path.exists(path):
        os.mkdir(path)
    for file in os.listdir(path):
        if not file.endswith('py'):
            continue
        try:
            import importlib.util as util
            spec = util.spec_from_file_location(file[:-3], os.path.join(path, file))
            mod = util.module_from_spec(spec)
            spec.loader.exec_module(mod)
        except ImportError:
            from importlib import import_module
            sys.path.insert(0, path)
            try:
                import_module(file[:-3])
            except ModuleNotFoundError:
                pass