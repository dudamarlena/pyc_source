# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/procblock/procyaml.py
# Compiled at: 2010-10-14 14:04:21
"""
procyaml

Process YAML files to make them easier to write for procblock.

Specially, add __import_%(key)s tags, so we can embed YAML files inside of
each other, and order our data a bit more sanely.

ImportYaml() does the __import_ thing.

LoadYaml() does caching.  TODO(g): Mix this with that.

TODO(g): ImportYaml should cache, but needs to remember all the files it __load
    or __import imported, so that we can test all these files for changes as
    well.  Any of these files changing should invalidate the cache.
"""
import os, yaml, stat, logging, unidist
from unidist import stack
from unidist.log import log
from unidist import sharedstate
YAML_CACHE = {}
YAML_CACHE_TIME = {}

def Save(path, data):
    """Save this data to this path, in YAML format.
  Uses temp file to avoid clobbering the original and failing to complete.
  """
    temp_file = '%s.tmp' % path
    fp = open(temp_file, 'w')
    yaml.dump(data, fp)
    fp.close()
    os.rename(temp_file, path)


def Load(path):
    """**Deprecating in favor of ImportYaml(), which can recursively import.**
  
  TODO(g): Decommission LoadYaml from use...  Redundant in this module.
  
  Args:
    path: string, file to load
  """
    return LoadYaml(path)


def LoadYaml(path):
    """**Deprecating in favor of ImportYaml(), which can recursively import.**
  
  Wraps loading of files, so they can be cached, and the cache can be
  updated.
  
  Args:
    path: string, file to load
  """
    global YAML_CACHE
    if type(path) != str:
        log('Path is not a string: %s: %s' % (stack.Mini(4), path), logging.ERROR)
    if path in YAML_CACHE:
        if os.stat(path)[stat.ST_MTIME] == YAML_CACHE_TIME[path]:
            return YAML_CACHE[path]
    try:
        fp = open(path, 'r')
        data = yaml.load(fp.read())
        fp.close()
    except TypeError:
        log('Failed to load YAML file: %s' % path, logging.ERROR)
        raise

    if data != None:
        YAML_CACHE[path] = data
        timestamp = os.stat(path)[stat.ST_MTIME]
        YAML_CACHE_TIME[path] = timestamp
        sharedstate.Set('__internals.yaml', path, (data, timestamp))
    return data


def ImportYaml_ImportKey(data, cwd):
    """Recursive function to import keys into a YAML dictionary."""
    for key in data.keys():
        if key.startswith('__import__'):
            (_, import_key) = key.split('__import__', 1)
            log('Importing key: %s: %s' % (import_key, data[key]))
            import_filename = data[key]
            if not os.path.isfile(import_filename):
                if import_filename.startswith('/'):
                    raise Exception('ImportYaml: Cannot import key YAML: %s: %s: Absolute path file not found' % (key, import_filename))
                else:
                    import_filename = '%s/%s' % (cwd, import_filename)
                    if not os.path.isfile(import_filename):
                        raise Exception('ImportYaml: Cannot import key YAML: %s: %s: Appending to current working directory failed' % (key, import_filename))
            import_data = ImportYaml(import_filename, cwd=cwd)
            del data[key]
            if import_key in data and type(data[import_key]) == dict and type(import_data) == dict:
                data[import_key].update(import_data)
            else:
                data[import_key] = import_data
        elif key == '__load':
            load_data = ImportYaml(data[key], cwd=cwd)
            data.update(load_data)
            del data[key]
        elif type(data[key]) == dict:
            ImportYaml_ImportKey(data[key], cwd)


def Import(filename, cwd=None):
    """TODO(g): Migrate usage to this?  It's obvious it's a YAML file..."""
    return ImportYaml(filename, cwd=cwd)


def ImportYaml(filename, cwd=None):
    """Import this YAML file, and import recursively any sections marked with
  __import__name, where "name" will be updated as a dictionary, or replaced
  if not a dictionary.
  
  Args:
    filename: string, name of file to load
    cwd: string (optional), if present this is the current working directory
        of the first imported file
  
  Returns: data, typically a dictionary.  Contents of YAML file.
  """
    timestamp = os.stat(filename)[stat.ST_MTIME]
    if sharedstate.KeyExists('__internals.yaml', filename):
        (cache_data, cache_timestamp) = sharedstate.Get('__internals.yaml', filename)
        if cache_timestamp == timestamp:
            return cache_data
    log('Importing YAML: %s' % filename)
    fp = open(filename)
    data = yaml.load(fp)
    fp.close()
    if data == None:
        return {}
    else:
        if cwd == None:
            cwd = os.path.dirname(filename)
        if type(data) == dict:
            ImportYaml_ImportKey(data, cwd)
        timestamp = os.stat(filename)[stat.ST_MTIME]
        sharedstate.Set('__internals.yaml', filename, (data, timestamp))
        return data


def WalkTreeExtractTag(data, tag, extract_function):
    """Data the data tree looking for a tag.
  
  Args:
    data: arbitrary data to walk, really only works on dicts/sequences combos,
        but accepts any structure, and reads tags only from dicts (obviously)
    tag: string, the key to search for in whatever dicts are inside this
        arbitrarily nested data
    extract_function: function, a function of the arg format:
        Func(data, collected)
        Where data is the data found with the key of the tag variable, and
        collected is the dict we are passing around to collect results
  
  Returns: dict, keyed on whatever the extract_function used to store the data,
      values are whatever the extract data chose to store.
  """
    collected = {}
    if type(data) == dict or isinstance(data, unidist.threadsafedict.ThreadSafeDict):
        for key in data:
            if key == tag:
                extract_function(data[key], collected)
            elif type(data[key]) == dict or isinstance(data[key], unidist.threadsafedict.ThreadSafeDict):
                collected.update(WalkTreeExtractTag(data[key], tag, extract_function))
            elif type(data[key]) in (list, tuple) or isinstance(data[key], unidist.threadsafelist.ThreadSafeList):
                collected.update(WalkTreeExtractTag(data[key], tag, extract_function))

    elif type(data) in (list, tuple) or isinstance(data, unidist.threadsafelist.ThreadSafeList):
        for item in data:
            if type(item) == dict or isinstance(item, unidist.threadsafedict.ThreadSafeDict):
                collected.update(WalkTreeExtractTag(item, tag, extract_function))
            elif type(item) in (list, tuple) or isinstance(item, unidist.threadsafelist.ThreadSafeList):
                collected.update(WalkTreeExtractTag(item, tag, extract_function))

    return collected