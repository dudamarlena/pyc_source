# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parallel_run/tools.py
# Compiled at: 2014-01-13 21:46:50
from ConfigParser import ConfigParser
import imp, sys, types, chardet

class ConfigParser(ConfigParser):

    def optionxform(self, option_str):
        return option_str


def str2unicode(s):
    if isinstance(s, str):
        code = chardet.detect(s)
        if code['confidence'] > 0.5:
            return unicode(s, code['encoding'])
    return s


def config2dict(config_file, section=None, decode=False):
    u"""将配置文件的内容读进字典"""
    cf = ConfigParser()
    cf.read(config_file)
    sections = [
     section]
    if section is None:
        sections = cf.sections()
    ret_dic = {}
    for sec in sections:
        if decode:
            ret_dic[str2unicode(sec)] = dict(map(lambda seq: map(str2unicode, seq), cf.items(sec)))
        else:
            ret_dic[sec] = dict(cf.items(sec))

    if section is not None:
        return ret_dic.pop(str2unicode(section) if decode else section)
    return ret_dic


def load_module(name, path=None, add_to_sys=False):
    u"""动态导入或reload一个模块"""
    mod = imp.load_module(name, *imp.find_module(name, path))
    if add_to_sys:
        sys.modules[name] = mod
    return mod