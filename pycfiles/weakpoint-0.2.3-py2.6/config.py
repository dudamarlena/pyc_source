# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/weakpoint/config.py
# Compiled at: 2012-11-21 04:46:57
import yaml
from weakpoint.exceptions import ConfigException
from weakpoint.fs import File

class Config(dict):

    def __init__(self, string):
        super(Config, self).__init__()
        try:
            self.update(yaml.load(string))
        except yaml.YAMLError:
            raise ConfigException('YAML Error')
        except:
            raise ConfigException('Invalid config format.')