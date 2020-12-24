# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/misc/yaml_tool.py
# Compiled at: 2015-05-26 14:10:22
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def yaml_dump(obj):
    """
    Dump an object to yaml string, only basic python types are supported

    @return yaml string or `None` if failed
    """
    try:
        output = dump(obj, Dumper=Dumper)
    except Exception as e:
        print e
        output = None

    return output


def yaml_load(stream):
    """
    Load from yaml stream and create a new python object

    @return object or `None` if failed
    """
    try:
        obj = load(stream, Loader=Loader)
    except Exception as e:
        print e
        obj = None

    return obj


__all__ = [
 yaml_dump, yaml_load]