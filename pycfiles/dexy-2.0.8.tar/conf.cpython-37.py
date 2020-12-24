# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/commands/conf.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 1587 bytes
from dexy.commands.utils import default_config
from dexy.utils import defaults
from dexy.utils import file_exists
import dexy.exceptions, inspect, json, os, yaml

def conf_command(conf=defaults['config_file'], p=False):
    """
    Write a config file containing dexy's defaults.
    """
    if file_exists(conf):
        if not p:
            print(inspect.cleandoc('Config file %s already exists,\n        will print conf to stdout instead...' % conf))
            p = True
    else:
        config = default_config()
        del config['conf']
        yaml_help = inspect.cleandoc("# YAML config file for dexy.\n        # You can delete any lines you don't wish to customize.\n        # Options are same as command line options,\n        # for more info run 'dexy help -on dexy'.\n        ")
        if p:
            print(yaml.dump(config, default_flow_style=False))
        else:
            with open(conf, 'w') as (f):
                if conf.endswith('.yaml') or conf.endswith('.conf'):
                    f.write(yaml_help)
                    f.write(os.linesep)
                    f.write(yaml.dump(config, default_flow_style=False))
                else:
                    if conf.endswith('.json'):
                        json.dump(config, f, sort_keys=True, indent=4)
                    else:
                        msg = "Don't know how to write config file '%s'"
                        raise dexy.exceptions.UserFeedback(msg % conf)
            print("Config file has been written to '%s'" % conf)