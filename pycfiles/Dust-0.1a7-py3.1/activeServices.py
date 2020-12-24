# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dust/server/activeServices.py
# Compiled at: 2010-06-01 17:13:46
from dust.util.ymap import YamlMap
activeServices = {}
paths = YamlMap('config/activeServices.yaml')
for serviceName in paths.keys():
    moduleName, className = paths[serviceName]
    mod = __import__(moduleName)
    print('dynamic loading module: ' + str(dir(mod)))
    cls = mod[className]
    obj = cls()
    activeServices[serviceName] = obj