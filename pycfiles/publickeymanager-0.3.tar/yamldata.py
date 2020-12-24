# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/publickey/yamldata.py
# Compiled at: 2014-10-30 23:23:11
import yaml
empty = (None, )

def tags(entry):
    lst = entry.get('tags')
    if isinstance(lst, basestring):
        lst = [
         lst]
    return lst


def first_tag(entry):
    lst = tags(entry) or empty
    return lst[0]


def load(filepath):
    with open(filepath, 'r') as (fp):
        return yaml.safe_load(fp.read())


def _all(doc):
    return ((name, x) for name, x in doc.items() if 'hostname' in x)


def filter_by_tags(doc, tags):
    items = _all(doc)
    if tags:
        criterion = set(tags)

        def filter_by_tags(iterable):
            for name, x in iterable:
                _tags = x.get('tags')
                if isinstance(_tags, basestring):
                    _tags = [
                     _tags]
                if criterion <= set(_tags):
                    yield (
                     name, x)

        items = list(filter_by_tags(items))
    return items