# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ditz/files.py
# Compiled at: 2016-11-27 06:27:17
__doc__ = '\nFile utilities.\n'
import sys, yaml, codecs, six
from datetime import datetime
from .config import config

def read_file(path):
    """Read a file."""
    with codecs.open(path, 'rb', encoding='utf-8') as (fp):
        return fp.read()


def write_file(path, text):
    """Write a file."""
    with codecs.open(path, 'wb', encoding='utf-8') as (fp):
        fp.write(text)


def read_yaml_file(path):
    """Read YAML data from a file."""
    with codecs.open(path, 'rb', encoding='utf-8') as (fp):
        return read_yaml(fp)


def read_yaml(fp):
    """Read YAML data from a stream."""
    return yaml.safe_load(fp)


def read_object_file(path):
    """
    Read a YAML object from a file and normalize it.
    """
    obj = read_yaml_file(path)
    obj.normalize()
    return obj


def write_yaml_file(path, item):
    """
    Write an object to a YAML file.
    """
    with codecs.open(path, 'wb', encoding='utf-8') as (fp):
        fp.write('--- ')
        write_yaml(item, fp)


def write_yaml(item, fp=None, parent=None, level=0):
    """
    Write YAML data to a stream.
    """
    if fp is None:
        fp = sys.stdout
    value = six.text_type(item)
    tag = getattr(item, 'yaml_tag', None)
    indent = '  '
    if tag:
        fp.write(tag + ' \n')
        seenref = False
        for attr in item.attributes:
            if attr == 'id' and not seenref:
                fp.write('\n')
            fp.write(indent * (level - 1))
            fp.write('%s: ' % attr)
            obj = getattr(item, attr)
            if obj and attr == 'references':
                seenref = True
            write_yaml(obj, fp, item, level + 1)

    elif isinstance(item, dict):
        if parent:
            fp.write('\n')
        for key, obj in sorted(item.items()):
            fp.write(indent * (level - 1))
            fp.write('%s: ' % key)
            write_yaml(obj, fp, item, level + 1)

    elif isinstance(item, list):
        if len(item) > 0:
            newline = doindent = not isinstance(parent, list)
            if hasattr(parent, 'ditz_tag') and level > 1:
                level -= 1
            if newline:
                fp.write('\n')
            for obj in item:
                if doindent:
                    fp.write(indent * (level - 1))
                else:
                    doindent = True
                fp.write('- ')
                write_yaml(obj, fp, item, level + 1)

        else:
            fp.write('[]\n')
    elif isinstance(item, datetime):
        fp.write('%s Z\n' % six.text_type(item))
    elif '\n' in value:
        fp.write('|-\n')
        if isinstance(parent, list) and level > 1:
            level -= 1
        for line in value.split('\n'):
            fp.write(indent * level)
            fp.write(line + '\n')

    elif item is None:
        fp.write('\n')
    else:
        quote = False
        if not value:
            quote = True
        elif value[0] in '"{}[]':
            quote = True
        elif value[0] != ':' and ':' in value:
            quote = True
        elif '#' in value:
            quote = True
        else:
            try:
                float(value)
                quote = True
            except ValueError:
                pass

        if quote:
            value = '"' + value.replace('"', '\\"') + '"'
        fp.write(value + '\n')
    return


def write_config(conf, dirname='.'):
    """
    Write Ditz config file if required.
    """
    if config.getboolean('config', 'create_ditz_config'):
        conf.write(dirname)
        return True
    return False