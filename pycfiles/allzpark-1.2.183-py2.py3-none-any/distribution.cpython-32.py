# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__setup__/ally_plugin/distribution.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Feb 6, 2013\n\n@package: ally plugin\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the distribution controlled events for the plugins.\n'
from ally.container import ioc
from ally.container.impl.config import load, save, Config
from os.path import isfile
APP_NORMAL = 'normal'
APP_DEVEL = 'devel'

@ioc.config
def distribution_file_path():
    """ The name of the distribution file for the plugins deployments"""
    return 'distribution.properties'


@ioc.config
def application_mode():
    """
    The distribution application mode, the possible values are:
    "normal" - the application behaves as the normal production instance, this means:
            * the deployments are executed every time, as it should normally would
            * the populates are executed only once as it should normally would

    "devel" - the application behaves as a development instance, this means:
            * the deployments are executed every time, as it should normally would
            * the populates are executed only once as it should normally would except those that are marked for development.
    """
    return APP_DEVEL


@ioc.entity
def markers():
    """ The markers for the executed events"""
    markers = {}
    if isfile(distribution_file_path()):
        with open(distribution_file_path(), 'r') as (f):
            for key, value in load(f).items():
                markers['__plugin__.%s' % key] = value

    return markers


def persistMarkers(used):
    """ Persist the markers of the executed events"""
    assert isinstance(used, set), 'Invalid used %s' % used
    plen = len('__plugin__.')
    configs = {}
    for name, value in markers().items():
        if name in used:
            group = 'current markers'
        else:
            group = 'unused markers'
        configs[name[plen:]] = Config(name, value, group)

    with open(distribution_file_path(), 'w') as (f):
        save(configs, f)