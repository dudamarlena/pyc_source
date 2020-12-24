# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hashdb/hashdb_config_updatedb.py
# Compiled at: 2011-01-06 01:43:26
from hashdb_output import log
from hashdb_config_base import *
import re

def parse_config_updatedb(filename='/etc/updatedb.conf'):
    re_namevalue = re.compile('\n        ^                 # begining of line\n        \\s*               # whitespace\n        (?P<n>[a-zA-Z_]+) # name\n        \\s*               # whitespace\n        =                 # =\n        \\s*               # whitespace\n        "(?P<v>.*?)"      # quoted value\n        .*                # whitespace/garbage/ignored\n        $                 # end of string\n        ', re.VERBOSE)
    parse_mappings = {'prunefs': (
                 'skip_fstypes', parse_text__filenames), 
       'prunenames': (
                    'skip_names', parse_text__filenames), 
       'prunepaths': (
                    'skip_paths', parse_text__filenames), 
       'prune_bind_mounts': (
                           'skip_binds', parse_text__boolean)}
    try:
        settings = {}
        with open(filename, 'rt') as (f):
            for (name, value) in [ (m.group('n').lower(), m.group('v')) for m in [ re_namevalue.match(line) for line in f.readlines() ] if m != None ]:
                if name not in parse_mappings:
                    log.warning('warning: unknown setting (%s) in updatedb config (%s)' % (name, filename))
                else:
                    (target, fparse) = parse_mappings[name]
                    settings[target] = fparse(value)

        return settings
    except IOError, ex:
        log.warning('warning: unable to open updatedb config file (%s): %s' % (filename, ex))
        print >> stderr, 'warning: %s' % ex
        return {}

    return