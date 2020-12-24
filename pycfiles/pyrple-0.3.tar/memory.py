# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/memory.py
# Compiled at: 2017-08-29 09:44:06
import os
from collections import OrderedDict
from shutil import copyfile
import numpy as np, time
from qtpy import QtCore
from . import default_config_dir, user_config_dir
from .pyrpl_utils import time
import logging
logger = logging.getLogger(name=__name__)

class UnexpectedSaveError(RuntimeError):
    pass


try:
    raise
    import ruamel.yaml
    ruamel.yaml.RoundTripDumper.add_representer(np.float64, lambda dumper, data: dumper.represent_float(float(data)))
    ruamel.yaml.RoundTripDumper.add_representer(complex, lambda dumper, data: dumper.represent_str(str(data)))
    ruamel.yaml.RoundTripDumper.add_representer(np.complex128, lambda dumper, data: dumper.represent_str(str(data)))
    ruamel.yaml.RoundTripDumper.add_representer(np.ndarray, lambda dumper, data: dumper.represent_list(list(data)))

    def load(f):
        return ruamel.yaml.load(f, ruamel.yaml.RoundTripLoader)


    def save(data, stream=None):
        return ruamel.yaml.dump(data, stream=stream, Dumper=ruamel.yaml.RoundTripDumper, default_flow_style=False)


except:
    logger.debug('ruamel.yaml could not be imported. Using yaml instead. Comments in config files will be lost.')
    import yaml

    def load(stream, Loader=yaml.SafeLoader, object_pairs_hook=OrderedDict):

        class OrderedLoader(Loader):
            pass

        def construct_mapping(loader, node):
            loader.flatten_mapping(node)
            return object_pairs_hook(loader.construct_pairs(node))

        OrderedLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)
        return yaml.load(stream, OrderedLoader)


    def save(data, stream=None, Dumper=yaml.SafeDumper, default_flow_style=False, encoding='utf-8', **kwds):

        class OrderedDumper(Dumper):
            pass

        def _dict_representer(dumper, data):
            return dumper.represent_mapping(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, data.items())

        OrderedDumper.add_representer(OrderedDict, _dict_representer)
        OrderedDumper.add_representer(np.float64, lambda dumper, data: dumper.represent_float(float(data)))
        OrderedDumper.add_representer(complex, lambda dumper, data: dumper.represent_str(str(data)))
        OrderedDumper.add_representer(np.complex128, lambda dumper, data: dumper.represent_str(str(data)))
        OrderedDumper.add_representer(np.ndarray, lambda dumper, data: dumper.represent_list(list(data)))
        if isinstance(data, dict) and not isinstance(data, OrderedDict):
            data = OrderedDict(data)
        return yaml.dump(data, stream=stream, Dumper=OrderedDumper, default_flow_style=default_flow_style, encoding=encoding, **kwds)


def isbranch(obj):
    return isinstance(obj, dict) or isinstance(obj, list)


def _get_filename(filename=None):
    """ finds the correct path and name of a config file """
    if isinstance(filename, MemoryTree):
        return filename._filename
    if not filename.endswith('.yml'):
        filename = filename + '.yml'
    p, f = os.path.split(filename)
    for path in [p, user_config_dir, default_config_dir]:
        file = os.path.join(path, f)
        if os.path.isfile(file):
            return file

    return os.path.join(user_config_dir, f)


def get_config_file(filename=None, source=None):
    """ returns the path to a valid, existing config file with possible source specification """
    if filename is None:
        return filename
    else:
        filename = _get_filename(filename)
        if os.path.isfile(filename):
            p, f = os.path.split(filename)
            if p == default_config_dir:
                dest = os.path.join(user_config_dir, f)
                copyfile(filename, dest)
                return dest
            return filename
        if source is not None:
            source = _get_filename(source)
            if os.path.isfile(source):
                logger.debug('File ' + filename + " not found. New file created from source '%s'. " % source)
                copyfile(source, filename)
                return filename
        with open(filename, mode='w'):
            pass
        logger.debug('File ' + filename + ' not found. New file created. ')
        return filename


class MemoryBranch(object):
    """Represents a branch of a memoryTree

    All methods are preceded by an underscore to guarantee that tab
    expansion of a memory branch only displays the available subbranches or
    leaves. A memory tree is a hierarchical structure. Nested dicts are
    interpreted as subbranches.

    Parameters
    ----------
    parent: MemoryBranch
        parent is the parent MemoryBranch
    branch: str
        branch is a string with the name of the branch to create
    defaults: list
        list of default branches that are used if requested data is not
        found in the current branch

    Class members
    -----------
    all properties without preceeding underscore are config file entries

    _data:      the raw data underlying the branch. Type depends on the
                loader and can be dict, OrderedDict or CommentedMap
    _dict:      similar to _data, but the dict contains all default
                branches
    _defaults:  list of MemoryBranch objects in order of decreasing
                priority that are used as defaults for the Branch.
                Changing the default values from the software will replace
                the default values in the current MemoryBranch but not
                alter the underlying default branch. Changing the
                default branch when it is not overridden by the current
                MemoryBranch results in an effective change in the branch.
    _keys:      same as _dict._keys()
    _update:    updates the branch with another dict
    _pop:       removes a value/subbranch from the branch
    _root:      the MemoryTree object (root) of the tree
    _parent:    the parent of the branch
    _branch:    the name of the branch
    _get_or_create: creates a new branch and returns it. Same as branch[newname]=dict(), but also supports nesting,
                e.g. newname="lev1.lev2.level3"
    _fullbranchname: returns the full path from root to the branch
    _getbranch: returns a branch by specifying its path, e.g. 'b1.c2.d3'
    _rename:    renames the branch
    _reload:    attempts to reload the data from disc
    _save:      attempts to save the data to disc

    If a subbranch or a value is requested but does not exist in the current MemoryTree, a KeyError is raised.
    """

    def __init__(self, parent, branch):
        self._parent = parent
        self._branch = branch
        self._update_instance_dict()

    def _update_instance_dict(self):
        data = self._data
        if isinstance(data, dict):
            for k in self.__dict__.keys():
                if k not in data and not k.startswith('_'):
                    self.__dict__.pop(k)

            for k in data.keys():
                self.__dict__[k] = None

        return

    @property
    def _data(self):
        """ The raw data (OrderedDict) or Mapping of the branch """
        return self._parent._data[self._branch]

    @_data.setter
    def _data(self, value):
        logger.warning('You are directly modifying the data of MemoryBranch %s to %s.', self._fullbranchname, str(value))
        self._parent._data[self._branch] = value

    def _keys(self):
        if isinstance(self._data, list):
            return range(self.__len__())
        else:
            return self._data.keys()

    def _update(self, new_dict):
        if isinstance(self._data, list):
            raise NotImplementedError
        self._data.update(new_dict)
        self._save()
        for k in new_dict:
            self.__dict__[k] = None

        return

    def __getattribute__(self, name):
        """ implements the dot notation.
        Example: self.subbranch.leaf returns the item 'leaf' of 'subbranch' """
        if name.startswith('_'):
            return super(MemoryBranch, self).__getattribute__(name)
        else:
            return self[name]

    def __getitem__(self, item):
        """
        __getitem__ bypasses the higher-level __getattribute__ function and provides
        direct low-level access to the underlying dictionary.
        This is much faster, as long as no changes have been made to the config
        file.
        """
        self._reload()
        if isinstance(item, str) and '.' in item:
            item, subitem = item.split('.', 1)
            return self[item][subitem]
        else:
            attribute = self._data[item]
            if isbranch(attribute):
                return MemoryBranch(self, item)
            return attribute

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super(MemoryBranch, self).__setattr__(name, value)
        else:
            self[name] = value

    def __setitem__(self, item, value):
        """
        creates a new entry, overriding the protection provided by dot notation
        if the value of this entry is of type dict, it becomes a MemoryBranch
        new values can be added to the branch in the same manner
        """
        if isbranch(value):
            if isinstance(value, list):
                self._set_data(item, [])
                subbranch = self[item]
                for k, v in enumerate(value):
                    subbranch[k] = v

            else:
                self._set_data(item, dict())
                subbranch = self[item]
                for k, v in value.items():
                    subbranch[k] = v

        else:
            self._set_data(item, value)
        if self._root._WARNING_ON_SAVE or self._root._ERROR_ON_SAVE:
            logger.warning('Issuing call to MemoryTree._save after %s.%s=%s', self._branch, item, value)
        self._save()
        self.__dict__[item] = None
        return

    def _set_data(self, item, value):
        """
        helper function to manage setting list entries that do not exist
        """
        if isinstance(self._data, list) and item == len(self._data):
            self._data.append(value)
        else:
            self._data[item] = value

    def _pop(self, name):
        """
        remove an item from the branch
        """
        value = self._data.pop(name)
        if name in self.__dict__.keys():
            self.__dict__.pop(name)
        self._save()
        return value

    def _rename(self, name):
        self._parent[name] = self._parent._pop(self._branch)
        self._save()

    def _get_or_create(self, name):
        """
        creates a new subbranch with name=name if it does not exist already
        and returns it. If name is a branch hierarchy such as
        "subbranch1.subbranch2.subbranch3", all three subbranch levels
        are created
        """
        if isinstance(name, int):
            if name == 0 and len(self) == 0:
                self._parent._data[self._branch] = []
            if name >= len(self):
                self[name] = dict()
            return self[name]
        else:
            currentbranch = self
            for subbranchname in name.split('.'):
                if subbranchname not in currentbranch._data.keys():
                    currentbranch[subbranchname] = dict()
                currentbranch = currentbranch[subbranchname]

            return currentbranch

    def _erase(self):
        """
        Erases the current branch
        """
        self._parent._pop(self._branch)
        self._save()

    @property
    def _root(self):
        """
        returns the parent highest in hierarchy (the MemoryTree object)
        """
        parent = self
        while parent != parent._parent:
            parent = parent._parent

        return parent

    @property
    def _fullbranchname(self):
        parent = self._parent
        branchname = self._branch
        while parent != parent._parent:
            branchname = parent._branch + '.' + branchname
            parent = parent._parent

        return branchname

    def _reload(self):
        """ reload data from file"""
        self._parent._reload()

    def _save(self):
        """ write data to file"""
        self._parent._save()

    def _get_yml(self, data=None):
        """
        :return: returns the yml code for this branch
        """
        return save(self._data if data is None else data).decode('utf-8')

    def _set_yml(self, yml_content):
        """
        :param yml_content: sets the branch to yml_content
        :return: None
        """
        branch = load(yml_content)
        self._parent._data[self._branch] = branch
        self._save()

    def __len__(self):
        return len(self._data)

    def __contains__(self, item):
        return item in self._data

    def __repr__(self):
        return 'MemoryBranch(' + str(self._keys()) + ')'

    def __add__(self, other):
        """
        makes it possible to add list-like memory tree to a list
        """
        if not isinstance(self._data, list):
            raise NotImplementedError
        return self._data + other

    def __radd__(self, other):
        """
        makes it possible to add list-like memory tree to a list
        """
        if not isinstance(self._data, list):
            raise NotImplementedError
        return other + self._data


class MemoryTree(MemoryBranch):
    """
    The highest level of a MemoryBranch construct. All attributes of this
    object that do not start with '_' are other MemoryBranch objects or
    Leaves, i.e. key - value pairs.

    Parameters
    ----------
    filename: str
        The filename of the .yml file defining the MemoryTree structure.
    """
    _data = None
    _WARNING_ON_SAVE = False
    _ERROR_ON_SAVE = False

    def __init__(self, filename=None, source=None, _loadsavedeadtime=3.0):
        self._loadsavedeadtime = _loadsavedeadtime
        self._filename = get_config_file(filename, source)
        if filename is None:
            self._filename = filename
            self._data = OrderedDict()
        self._lastsave = time()
        self._savetimer = QtCore.QTimer()
        self._savetimer.setInterval(self._loadsavedeadtime * 1000)
        self._savetimer.setSingleShot(True)
        self._savetimer.timeout.connect(self._write_to_file)
        self._load()
        self._save_counter = 0
        self._write_to_file_counter = 0
        super(MemoryTree, self).__init__(self, '')
        return

    @property
    def _buffer_filename(self):
        """ makes a temporary file to ensure modification of config file is atomic (double-buffering like operation...)"""
        return self._filename + '.tmp'

    def _load(self):
        """ loads data from file """
        if self._filename is None:
            return
        else:
            logger.debug('Loading config file %s', self._filename)
            with open(self._filename) as (f):
                self._data = load(f)
            self._mtime = os.path.getmtime(self._filename)
            self._lastreload = time()
            if self._data is None:
                self._data = OrderedDict()
            to_remove = []
            for name in self.__dict__:
                if not name.startswith('_') and name not in self._data:
                    to_remove.append(name)

            for name in to_remove:
                self.__dict__.pop(name)

            self.__dict__.update(self._data)
            return

    def _reload(self):
        """
        reloads data from file if file has changed recently
        """
        if self._filename is None:
            return
        else:
            if time() > self._lastreload + self._loadsavedeadtime:
                self._lastreload = time()
                logger.debug('Checking change time of config file...')
                if self._mtime != os.path.getmtime(self._filename):
                    logger.debug('Loading because mtime %s != filetime %s', self._mtime)
                    self._load()
                else:
                    logger.debug('... no reloading required')
            return

    def _write_to_file(self):
        """
        Immmediately writes the content of the memory tree to file
        """
        if hasattr(self, '_savetimer') and self._savetimer.isActive():
            self._savetimer.stop()
        self._lastsave = time()
        self._write_to_file_counter += 1
        logger.debug('Saving config file %s', self._filename)
        if self._filename is None:
            return
        else:
            if self._mtime != os.path.getmtime(self._filename):
                logger.warning('Config file has recently been changed on your ' + 'harddisk. These changes might have been ' + 'overwritten now.')
            copyfile(self._filename, self._filename + '.bak')
            try:
                f = open(self._buffer_filename, mode='w')
                save(self._data, stream=f)
                f.flush()
                os.fsync(f.fileno())
                f.close()
                os.unlink(self._filename)
                os.rename(self._buffer_filename, self._filename)
            except:
                copyfile(self._filename + '.bak', self._filename)
                logger.error('Error writing to file. Backup version was restored.')
                raise

            self._mtime = os.path.getmtime(self._filename)
            return

    def _save(self, deadtime=None):
        """
        A call to this function means that the state of the tree has changed
        and needs to be saved eventually. To reduce system load, the delay
        between two writes will be at least deadtime (defaults to
        self._loadsavedeadtime if None)
        """
        if self._ERROR_ON_SAVE:
            raise UnexpectedSaveError('Save to config file should not happen now')
        if self._WARNING_ON_SAVE:
            logger.warning('Save counter has just been increased to %d.', self._save_counter)
        self._save_counter += 1
        if deadtime is None:
            deadtime = self._loadsavedeadtime
        if self._lastsave + deadtime < time():
            self._write_to_file()
        elif not self._savetimer.isActive():
            self._savetimer.start()
        return

    @property
    def _filename_stripped(self):
        try:
            return os.path.split(self._filename)[1].split('.')[0]
        except:
            return 'default'