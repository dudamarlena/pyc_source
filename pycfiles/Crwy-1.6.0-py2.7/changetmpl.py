# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/crwy/changetmpl.py
# Compiled at: 2020-02-03 23:11:43
from string import Template
try:
    import ConfigParser
except ImportError:
    from configparser import ConfigParser

def get_project_name():
    conf = ConfigParser()
    conf.read('crwy.cfg', encoding='utf-8')
    project_name = conf.get('project', 'project_name').encode('utf-8')
    return project_name


def change_project_name(name, path):
    f = open(path, 'r')
    t = Template(f.read()).substitute(project_name=name)
    return t


def change_spider_name(name, path):
    f = open(path, 'r')
    class_name = name.capitalize()
    spider_name = name
    project_name = get_project_name()
    t = Template(f.read()).substitute(class_name=class_name, spider_name=spider_name, project_name=project_name)
    return t