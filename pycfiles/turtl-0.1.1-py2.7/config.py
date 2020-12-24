# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/turtl/config.py
# Compiled at: 2009-08-21 14:13:15
from yaml import load

def loadConfigFromFile(filepath):
    """
    Load the configuration options from a filepath

    @param filepath: The filepath to a configuration file.
    @type filepath: C{twisted.python.filepath.FilePath}
    """
    return loadConfigFromString(filepath.getContent())


def loadConfigFromString(s):
    """
    Load the configuration options from a string.

    @param s: a C{str} that contains the yaml formatted
                    configuration
    @type s: yaml formatted C{str}

    @returns: a tuple of hostname and L{engine.ThrottlingDeferred}s
                and the default behavior for unknown urls.
    """
    from turtl import engine
    loaded = load(s)
    rest = loaded.pop('filter-rest', True)
    port = loaded.pop('port', 8080)
    defaults = loaded.pop('defaults', {})
    defaults.update({'calls': 1, 'interval': 1, 'concurrency': 10})
    urlmapping = {}
    for host, kwargs in loaded.iteritems():
        kw = {}
        kw.update(defaults)
        kw.update(kwargs)
        urlmapping[host] = engine.ThrottlingDeferred(**kw)

    return (urlmapping, rest, port)