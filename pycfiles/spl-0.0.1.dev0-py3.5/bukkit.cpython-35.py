# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spl/bukkit.py
# Compiled at: 2016-12-14 10:21:13
# Size of source mod 2**32: 248 bytes
import yaml
from zipfile import ZipFile

def get_data_directory(plugin_jar):
    with ZipFile(plugin_jar, 'r') as (jar):
        with jar.open('plugin.yml', 'r') as (plugin_yml):
            yml = yaml.load(plugin_yml)
            return yml['name']