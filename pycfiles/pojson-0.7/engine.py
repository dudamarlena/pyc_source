# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pojen/engine.py
# Compiled at: 2016-08-26 17:47:53
import builders
java_types = {bool: 'boolean', 
   float: 'float', 
   int: 'int', 
   str: 'String'}
java_types_array = {bool: 'Boolean', 
   float: 'Float', 
   int: 'Integer', 
   str: 'String'}

def generate_classes(structures, public_fields=False, getset=True):
    classes = []
    for classname, struct, imports in structures:
        t_class = builders.generate_class(classname, struct, public_fields, getset, imports)
        classes.append((classname, t_class))

    return classes


def prepare_structure(obj, classname=''):
    classname = builders.upperfirst(classname)
    classes = []
    element = {}
    imports_strings = []
    imports = {}
    classes.append((classname, element, imports_strings))
    for key, value in obj.items():
        key = normalize_key_case(key)
        if type(value) == dict:
            dt = prepare_structure(value, key)
            classes += dt
            element[key] = key.title()
        elif type(value) == list:
            if len(value) > 0 and type(value[0]) == dict:
                ls = prepare_structure(value[0], key)
                classes += ls
                imports['java.util.ArrayList'] = True
                element[key] = ('ArrayList<{}>').format(key.title())
            elif len(value) > 0:
                imports['java.util.ArrayList'] = True
                element[key] = ('ArrayList<{}>').format(java_types_array[infer_type(value[0])])
            else:
                imports['java.util.ArrayList'] = True
                element[key] = 'ArrayList<String>'
        else:
            element[key] = java_types[infer_type(value)]

    for key in imports:
        imports_strings.append(key)

    if classes[0][0] == '' and len(classes[0][1]) == 1:
        classes = classes[1:]
    return classes


def normalize_key_case(key):
    words = key.split('_')
    if len(words) == 1:
        return words[0]
    else:
        words = map(str, words)
        words = [words[0]] + map(str.title, words[1:])
        return ('').join(words)


def infer_type(obj):
    if obj == 'true' or obj == 'false':
        return bool
    if can_parse_float(obj):
        return float
    else:
        if can_parse_int(obj):
            return int
        return str


def can_parse_int(num):
    if type(num) == int:
        return True
    if type(num) == str:
        try:
            int(num)
        except ValueError:
            return False

        return True


def can_parse_float(num):
    if type(num) == float:
        return True
    if type(num) == str:
        if len(num.split('.')) == 1:
            return False
        try:
            float(num)
        except ValueError:
            return False

        return True