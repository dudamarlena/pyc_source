# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/bin/pytutor/pg_encoder.py
# Compiled at: 2014-02-02 09:23:12
FLOAT_PRECISION = 4
import re, types, sys
typeRE = re.compile("<type '(.*)'>")
classRE = re.compile("<class '(.*)'>")
import inspect
is_python3 = sys.version_info[0] == 3
if is_python3:
    long = None

def is_class(dat):
    """Return whether dat is a class."""
    if is_python3:
        return isinstance(dat, type)
    else:
        return type(dat) in (types.ClassType, types.TypeType)


def is_instance(dat):
    """Return whether dat is an instance of a class."""
    if is_python3:
        return isinstance(type(dat), type) and not isinstance(dat, type)
    else:
        return type(dat) == types.InstanceType or classRE.match(str(type(dat)))


def get_name(obj):
    """Return the name of an object."""
    if hasattr(obj, '__name__'):
        return obj.__name__
    return get_name(type(obj))


class ObjectEncoder:

    def __init__(self):
        self.encoded_heap_objects = {}
        self.id_to_small_IDs = {}
        self.cur_small_ID = 1

    def get_heap(self):
        return self.encoded_heap_objects

    def reset_heap(self):
        self.encoded_heap_objects = {}

    def set_function_parent_frame_ID(self, ref_obj, enclosing_frame_id):
        assert ref_obj[0] == 'REF'
        func_obj = self.encoded_heap_objects[ref_obj[1]]
        assert func_obj[0] == 'FUNCTION'
        func_obj[-1] = enclosing_frame_id

    def encode(self, dat, get_parent):
        """Encode a data value DAT using the GET_PARENT function for parent ids."""
        if type(dat) in (int, long, float, str, bool, type(None)):
            if type(dat) is float:
                return round(dat, FLOAT_PRECISION)
            else:
                return dat

        else:
            my_id = id(dat)
            try:
                my_small_id = self.id_to_small_IDs[my_id]
            except KeyError:
                my_small_id = self.cur_small_ID
                self.id_to_small_IDs[my_id] = self.cur_small_ID
                self.cur_small_ID += 1

        del my_id
        ret = [
         'REF', my_small_id]
        if my_small_id in self.encoded_heap_objects:
            return ret
        else:
            new_obj = []
            self.encoded_heap_objects[my_small_id] = new_obj
            typ = type(dat)
            if typ == list:
                new_obj.append('LIST')
                for e in dat:
                    new_obj.append(self.encode(e, get_parent))

            else:
                if typ == tuple:
                    new_obj.append('TUPLE')
                    for e in dat:
                        new_obj.append(self.encode(e, get_parent))

                elif typ == set:
                    new_obj.append('SET')
                    for e in dat:
                        new_obj.append(self.encode(e, get_parent))

                elif typ == dict:
                    new_obj.append('DICT')
                    for k, v in dat.items():
                        if k not in ('__module__', '__return__', '__locals__'):
                            new_obj.append([self.encode(k, get_parent), self.encode(v, get_parent)])

                elif typ in (types.FunctionType, types.MethodType):
                    if is_python3:
                        argspec = inspect.getfullargspec(dat)
                    else:
                        argspec = inspect.getargspec(dat)
                    printed_args = [ e for e in argspec.args ]
                    if argspec.varargs:
                        printed_args.append('*' + argspec.varargs)
                    if is_python3:
                        if argspec.varkw:
                            printed_args.append('**' + argspec.varkw)
                        if argspec.kwonlyargs:
                            printed_args.extend(argspec.kwonlyargs)
                    elif argspec.keywords:
                        printed_args.append('**' + argspec.keywords)
                    func_name = get_name(dat)
                    pretty_name = func_name + '(' + (', ').join(printed_args) + ')'
                    encoded_val = ['FUNCTION', pretty_name, None]
                    if get_parent:
                        enclosing_frame_id = get_parent(dat)
                        encoded_val[2] = enclosing_frame_id
                    new_obj.extend(encoded_val)
                elif typ is types.BuiltinFunctionType:
                    pretty_name = get_name(dat) + '(...)'
                    new_obj.extend(['FUNCTION', pretty_name, None])
                elif is_class(dat) or is_instance(dat):
                    self.encode_class_or_instance(dat, new_obj)
                elif typ is types.ModuleType:
                    new_obj.extend(['module', dat.__name__])
                else:
                    typeStr = str(typ)
                    m = typeRE.match(typeStr)
                    if not m:
                        m = classRE.match(typeStr)
                    assert m, typ
                    new_obj.extend([m.group(1), str(dat)])
                return ret
            return

    def encode_class_or_instance(self, dat, new_obj):
        """Encode dat as a class or instance."""
        if is_instance(dat):
            if hasattr(dat, '__class__'):
                class_name = get_name(dat.__class__)
            else:
                class_name = get_name(type(dat))
            new_obj.extend(['INSTANCE', class_name])
            if class_name == 'module':
                return
        else:
            superclass_names = [ e.__name__ for e in dat.__bases__ if e is not object ]
            new_obj.extend(['CLASS', get_name(dat), superclass_names])
        hidden = ('__doc__', '__module__', '__return__', '__dict__', '__locals__',
                  '__weakref__')
        if hasattr(dat, '__dict__'):
            user_attrs = sorted([ e for e in dat.__dict__ if e not in hidden ])
        else:
            user_attrs = []
        for attr in user_attrs:
            new_obj.append([self.encode(attr, None), self.encode(dat.__dict__[attr], None)])

        return