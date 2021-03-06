# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/cosmin/workspace/github/cleanmymac/build/lib/cleanmymac/registry.py
# Compiled at: 2016-02-15 15:07:48
# Size of source mod 2**32: 5204 bytes
import os
from tabulate import tabulate
from yaml import load
from functools import partial
from pkg_resources import iter_entry_points
from cleanmymac.util import yaml_files
from cleanmymac.builtins import BUILTINS_PATH
from cleanmymac.log import debug, error
from cleanmymac.constants import TARGET_ENTRY_POINT, VALID_TARGET_TYPES, TYPE_TARGET_CMD, TYPE_TARGET_DIR, GLOBAL_CONFIG_FILE
from cleanmymac.schema import validate_yaml_target
from cleanmymac.target import Target, YamlShellCommandTarget, YamlDirTarget
__TARGETS__ = {}
__YAML_TYPES__ = {TYPE_TARGET_CMD: YamlShellCommandTarget, 
 TYPE_TARGET_DIR: YamlDirTarget}

def load_target(yaml_file, config, update=False, verbose=False, strict=True):
    """
    load a target given its description from a **YAML** file.
    The file is validated according to its type before loading.

    :param str yaml_file: a valid path to a **YAML** file
    :param dict config: the global configuration dictionary
    :param bool update: specify whether to perform update before cleanup
    :param bool verbose: toggle verbosity
    :return: the target
    :rtype: :class:`cleanmymac.target.Target`
    """
    with open(yaml_file, 'r+') as (DESC):
        try:
            description = load(DESC)
            description = validate_yaml_target(description, strict=strict)
            _type = description['type']
            if _type not in VALID_TARGET_TYPES:
                error('unknown yaml target type: "{0}", valid options are: {1}'.format(_type, VALID_TARGET_TYPES))
                return
            else:
                target_class = __YAML_TYPES__[_type]
                if not issubclass(target_class, Target):
                    error('expected a subclass of Target for "{0}", instead got: "{1}"'.format(os.path.basename(yaml_file), target_class))
                    return
                if not config:
                    config = {}
                config['spec'] = description['spec']
                return target_class(config, update=update, verbose=verbose)
        except Exception as e:
            error('Error loading configuration: "{0}". Reason: {1}'.format(yaml_file, e))
            if strict:
                raise e
            return


def register_target(name, target):
    """
    register a target type to a given target name

    :param str name: the target name (case sensitive)
    :param target: the target to register
    :type target: :class:`cleanmymac.target.Target`
    """
    global __TARGETS__
    if issubclass(target, Target):
        debug('registering : {0}'.format(name))
        __TARGETS__[name] = target
    else:
        error('target {0} is not of type Target, instead got: {1}'.format(name, target))


def register_yaml_targets(path):
    """
    scans and registers all valid **YAML** defined targets in `path`. The name of the
    **YAML** file (without extension) becomes the target name

    :param str path: a valid directory
    """
    for name, yaml_file in yaml_files(path):
        if os.path.basename(yaml_file) == GLOBAL_CONFIG_FILE:
            pass
        else:
            debug('registering : {0}'.format(name))
            __TARGETS__[name] = partial(load_target, yaml_file)


def get_target(name):
    """
    get a registered target

    :param str name: the target name
    :return: the target
    :rtype: :class:`cleanmymac.target.Target`
    """
    try:
        return __TARGETS__[name]
    except KeyError:
        error('no target found for: {0}'.format(name))
        return


def iter_targets():
    """
    generator over all registered targets

    :return: pairs of (name: target)
    """
    for name, target in __TARGETS__.iteritems():
        yield (
         name, target)


def get_targets_as_table(simple=True, fancy=False):
    headers = ['Name', 'Type']

    def row(name, target):
        data = [
         name.upper()]
        t = target(None, update=False, verbose=False, strict=False)
        data.append(t.__class__.__name__ if simple else t.__class__)
        return data

    return tabulate([row(name, target) for name, target in __TARGETS__.iteritems()], headers=headers, tablefmt='fancy_grid' if fancy else 'orgtbl')


register_yaml_targets(BUILTINS_PATH)
debug('looking for registered cleanup targets...')
for ep in iter_entry_points(TARGET_ENTRY_POINT):
    debug('found: {0}'.format(ep))
    register_target(ep.name, ep.load())