# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rnix/workspace/touch.server/devsrc/yafowil.widget.array/src/yafowil/widget/array/example.py
# Compiled at: 2015-12-13 13:41:50
from yafowil.base import factory
DOC_ARRAY_WITH_LEAFS = "\nArray with single fields as array entries\n-----------------------------------------\n\nArray containing single field entries. Preset value is expected as list.\n\n.. code-block:: python\n\n    value = ['1', '2', '3']\n    array = factory('#array', value=value, props={\n        'label': 'My Array',\n        'help': 'I am an array',\n        'required': 'Array must at least contain one entry',\n    })\n    array['field'] = factory('#arrayfield:text', props={\n        'label': 'Entry',\n        'help': 'I am an array entry',\n        'required': 'Entry must not be empty',\n    })\n"

def array_with_leafs():
    form = factory('fieldset', name='yafowil.widget.array.array_with_leafs')
    value = ['1', '2', '3']
    arr = form['array'] = factory('#array', value=value, props={'label': 'My Array', 
       'help': 'I am an array', 
       'required': 'Array must at least contain one entry'})
    arr['field'] = factory('#arrayfield:text', props={'label': 'Entry', 
       'help': 'I am an array entry', 
       'required': 'Entry must not be empty'})
    return {'widget': form, 
       'doc': DOC_ARRAY_WITH_LEAFS, 
       'title': 'Single field array'}


DOC_ARRAY_WITH_COMPOUNDS = "\nArray with compounds as array entries\n-------------------------------------\n\nArray containing compound entries. Preset value is expected as list containing\ndictionaries addressing array child compound fields by key.\n\n.. code-block:: python\n\n    value = [\n        {'f1': 'Value 1.1 F1', 'f2': 'Value 1.2 F2'},\n        {'f1': 'Value 2.1 F1', 'f2': 'Value 2.2 F2'},\n    ]\n    array = factory('#array', value=value, props={\n        'label': 'Compound Array'\n        'required': 'Array must at least contain one entry',\n    })\n    compound = array['compound'] = factory('compound')\n    compound['f1'] = factory('#arrayfield:text', props={\n        'label': 'Field 1',\n    })\n    compound['f2'] = factory('#arrayfield:text', props={\n        'label': 'Field 2',\n        'required': 'Field 2 is required',\n    })\n"

def array_with_compounds():
    form = factory('fieldset', name='yafowil.widget.array.array_with_compounds')
    value = [{'f1': 'Value 1.1 F1', 'f2': 'Value 1.2 F2'}, {'f1': 'Value 2.1 F1', 'f2': 'Value 2.2 F2'}]
    arr = form['array'] = factory('#array', value=value, props={'label': 'Compound Array', 
       'required': 'Array must at least contain one entry'})
    comp = arr['compound'] = factory('compound')
    comp['f1'] = factory('#arrayfield:text', props={'label': 'Field 1'})
    comp['f2'] = factory('#arrayfield:text', props={'label': 'Field 2', 
       'required': 'Field 2 is required'})
    return {'widget': form, 
       'doc': DOC_ARRAY_WITH_COMPOUNDS, 
       'title': 'Compound field array'}


DOC_ARRAY_WITH_ARRAY_WITH_LEAFS = "\nArray in array with single fields\n---------------------------------\n\nArray in array containing single field entries. Preset value is a 2-dimensional\nlist\n\n.. code-block:: python\n\n    value = [['1', '2'], ['3', '4'], ['5', '6']]\n    array = factory('#array', value=value, props={\n        'label': 'Array',\n        'required': 'Array must at least contain one entry',\n    })\n    subarray = array['subarray'] = factory('error:array', props={\n        'label': 'Subarray',\n        'required': 'Subarray must at least contain one entry',\n    })\n    subarray['field'] = factory('#arrayfield:text', props={\n        'label': 'Entry',\n        'required': 'Entry must not be empty',\n    })\n"

def array_with_array_with_leafs():
    form = factory('fieldset', name='yafowil.widget.array_with_array_with_leafs')
    value = [['1', '2'], ['3', '4'], ['5', '6']]
    arr = form['array'] = factory('#array', value=value, props={'label': 'Array', 
       'required': 'Array must at least contain one entry'})
    subarr = arr['subarray'] = factory('error:array', props={'label': 'Subarray', 
       'required': 'Subarray must at least contain one entry'})
    subarr['field'] = factory('#arrayfield:text', props={'label': 'Entry', 
       'required': 'Entry must not be empty'})
    return {'widget': form, 
       'doc': DOC_ARRAY_WITH_ARRAY_WITH_LEAFS, 
       'title': 'Single field array in array'}


DOC_ARRAY_WITH_ARRAY_WITH_COMPOUNDS = "Array in array with compounds as array entries\n----------------------------------------------\n\nArray in array containing compound entries. Preset value is lists in list \ncontaining dictionaries addressing inner array child compound fields by key.\n\n.. code-block:: python\n\n    value = [\n        [{\n            'f1': 'Value 0.0 F1',\n            'f2': 'Value 0.0 F2',\n        }, {\n            'f1': 'Value 0.1 F1',\n            'f2': 'Value 0.1 F2',\n        }], [{\n            'f1': 'Value 1.0 F1',\n            'f2': 'Value 1.0 F2',\n        }, {\n            'f1': 'Value 1.1 F1',\n            'f2': 'Value 1.1 F2',\n        }]\n    ]\n    array = factory('#array', value=value, props={\n        'label': 'Array 1',\n    })\n    subarray = array['subarray'] = factory('array', props={\n        'label': 'Array 2',\n    })\n    compound = subarray['comp'] = factory('compound')\n    compound['f1'] = factory('#arrayfield:text', props={\n        'label': 'F1',\n    })\n    compound['f2'] = factory('#arrayfield:text', props={\n        'label': 'F2',\n        'required': 'F2 is required',\n    })\n"

def array_with_array_with_compounds():
    form = factory('fieldset', name='yafowil.widget.array_with_array_with_compounds')
    value = [
     [
      {'f1': 'Value 0.0 F1', 
         'f2': 'Value 0.0 F2'},
      {'f1': 'Value 0.1 F1', 
         'f2': 'Value 0.1 F2'}],
     [
      {'f1': 'Value 1.0 F1', 
         'f2': 'Value 1.0 F2'},
      {'f1': 'Value 1.1 F1', 
         'f2': 'Value 1.1 F2'}]]
    arr = form['array'] = factory('#array', value=value, props={'label': 'Array 1'})
    subarr = arr['subarray'] = factory('array', props={'label': 'Array 2'})
    comp = subarr['comp'] = factory('compound')
    comp['f1'] = factory('#arrayfield:text', props={'label': 'F1'})
    comp['f2'] = factory('#arrayfield:text', props={'label': 'F2', 
       'required': 'F2 is required'})
    return {'widget': form, 
       'doc': DOC_ARRAY_WITH_ARRAY_WITH_COMPOUNDS, 
       'title': 'Compound array in array'}


DOC_ARRAY_WITH_ARRAY_WITH_ARRAY_WITH_LEAFS = "3-Dimensional Array with single fields\n--------------------------------------\n\n3-Dimensional array containing single field entries. Preset value is a\n3-dimensional list\n\n.. code-block:: python\n\n    value = [[['1', '2'], ['3']], [['4', '5']]]\n    arr_1 = factory('#array', value=value, props={\n        'label': 'Array 1',\n        'help': 'This is Array 1',\n        'required': 'Array 1 must not be empty',\n    })\n    arr_2 = arr_1['array_2'] = factory('help:error:array', props={\n        'label': 'Array 2',\n        'help': 'This is Array 2',\n        'required': 'Array 2 must not be empty',\n    })\n    arr_3 = arr_2['array_3'] = factory('help:error:array', props={\n        'label': 'Array 3',\n        'help': 'This is Array 3',\n        'required': 'Array 3 must not be empty',\n    })\n    arr_3['field'] = factory('#arrayfield:text', props={\n        'label': 'Text Field',\n        'help': 'This is the text field',\n        'required': 'Text Field is required',\n    })\n"

def array_with_array_with_array_with_leafs():
    form = factory('fieldset', name='yafowil.widget.array_with_array_with_array_with_leafs')
    value = [[['1', '2'], ['3']], [['4', '5']]]
    arr_1 = form['array_1'] = factory('#array', value=value, props={'label': 'Array 1', 
       'help': 'This is Array 1', 
       'required': 'Array 1 must not be empty'})
    arr_2 = arr_1['array_2'] = factory('help:error:array', props={'label': 'Array 2', 
       'help': 'This is Array 2', 
       'required': 'Array 2 must not be empty'})
    arr_3 = arr_2['array_3'] = factory('help:error:array', props={'label': 'Array 3', 
       'help': 'This is Array 3', 
       'required': 'Array 3 must not be empty'})
    arr_3['textfield'] = factory('#arrayfield:text', props={'label': 'Text Field', 
       'help': 'This is the text field', 
       'required': 'Text Field is required'})
    return {'widget': form, 
       'doc': DOC_ARRAY_WITH_ARRAY_WITH_ARRAY_WITH_LEAFS, 
       'title': 'Single fields in 3-dimensional array'}


DOC_ARRAY_WITH_ARRAY_WITH_ARRAY_WITH_COMPOUNDS = "3-Dimensional Array with compounds\n----------------------------------\n\n3-Dimensional array containing compound entries. Preset value is a\n3-dimensional list containing dictionaries addressing most inner array child\ncompound fields by key.\n\n.. code-block:: python\n\n    value = [\n        [[{\n            'f1': 'Value F1',\n            'f2': 'Value F2',\n        }]], [[{\n            'f1': 'Value F1',\n            'f2': 'Value F2',\n        }]]\n    ]\n    arr_1 = factory('#array', value=value, props={\n        'label': 'Array 1',\n    })\n    arr_2 = arr_1['array_2'] = factory('array', props={\n        'label': 'Array 2',\n    })\n    arr_3 = arr_2['array_3'] = factory('array', props={\n        'label': 'Array 3',\n    })\n    compound = arr_3['comp'] = factory('compound')\n    compound['f1'] = factory('#arrayfield:text', props={\n        'label': 'F1',\n    })\n    compound['f2'] = factory('#arrayfield:text', props={\n        'label': 'F2',\n        'required': 'F2 is required',\n    })\n"

def array_with_array_with_array_with_compounds():
    form = factory('fieldset', name='yafowil.widget.array_with_array_with_array_with_compounds')
    value = [
     [
      [
       {'f1': 'Value F1', 
          'f2': 'Value F2'}]],
     [
      [
       {'f1': 'Value F1', 
          'f2': 'Value F2'}]]]
    arr_1 = form['array_1'] = factory('#array', value=value, props={'label': 'Array 1'})
    arr_2 = arr_1['array_2'] = factory('array', props={'label': 'Array 2'})
    arr_3 = arr_2['array_3'] = factory('array', props={'label': 'Array 3'})
    comp = arr_3['comp'] = factory('compound')
    comp['f1'] = factory('#arrayfield:text', props={'label': 'F1'})
    comp['f2'] = factory('#arrayfield:text', props={'label': 'F2', 
       'required': 'F2 is required'})
    return {'widget': form, 
       'doc': DOC_ARRAY_WITH_ARRAY_WITH_ARRAY_WITH_COMPOUNDS, 
       'title': 'Compounds in 3-dimensional array'}


def get_example():
    return [
     array_with_leafs(),
     array_with_compounds(),
     array_with_array_with_leafs(),
     array_with_array_with_compounds(),
     array_with_array_with_array_with_leafs(),
     array_with_array_with_array_with_compounds()]