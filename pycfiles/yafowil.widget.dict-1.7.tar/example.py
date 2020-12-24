# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rnix/workspace/yafowil.demo/devsrc/yafowil.widget.dict/src/yafowil/widget/dict/example.py
# Compiled at: 2018-02-02 03:08:23
from odict import odict
from yafowil.base import factory
DOC_MUTABLE_DICT = "\nMutable Dict\n------------\n\nDict where key/value pairs can be added, deleted and sorted.\n\n.. code-block:: python\n\n    value = odict()\n    value['foo'] = 'Foo'\n    value['bar'] = 'Bar'\n    dict = factory('#field:dict', value=value, props={\n        'label': 'Fill the dict',\n        'required': 'At least one entry is required',\n        'key_label': 'Key',\n        'value_label': 'Value'\n    })\n"

def mutable_dict():
    form = factory('fieldset', name='yafowil.widget.dict.mutable_dict')
    value = odict()
    value['foo'] = 'Foo'
    value['bar'] = 'Bar'
    form['dict'] = factory('#field:dict', value=value, props={'label': 'Fill the dict', 
       'required': 'At least one entry is required', 
       'key_label': 'Key', 
       'value_label': 'Value'})
    return {'widget': form, 
       'doc': DOC_MUTABLE_DICT, 
       'title': 'Mutable Dict'}


DOC_IMMUTABLE_DICT = "\nImmutable Dict\n--------------\n\nDict where only values can be edited.\n\n.. code-block:: python\n\n    value = odict()\n    value['baz'] = 'Baz'\n    value['bam'] = 'Bam'\n    dict = factory('#field:dict', value=value, props={\n        'label': 'Modify the dict',\n        'required': 'No Empty values allowed',\n        'static': True,\n        'key_label': 'Key',\n        'value_label': 'Value'\n    })\n"

def immutable_dict():
    form = factory('fieldset', name='yafowil.widget.dict.immutable_dict')
    value = odict()
    value['baz'] = 'Baz'
    value['bam'] = 'Bam'
    form['dict'] = factory('#field:dict', value=value, props={'label': 'Modify the dict', 
       'required': 'No Empty values allowed', 
       'static': True, 
       'key_label': 'Key', 
       'value_label': 'Value'})
    return {'widget': form, 
       'doc': DOC_IMMUTABLE_DICT, 
       'title': 'Imutable Dict'}


def get_example():
    return [
     mutable_dict(),
     immutable_dict()]