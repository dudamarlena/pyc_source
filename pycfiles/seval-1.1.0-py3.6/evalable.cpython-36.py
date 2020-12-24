# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\seval\evalable.py
# Compiled at: 2019-06-19 13:29:48
# Size of source mod 2**32: 1286 bytes
import ast, inspect, typing

class Evalable(type):
    _NODES_HANDLERS = {}

    def __new__(cls, name, bases, classdict, *, evalable_nodes):
        new_handlers = []
        for node in evalable_nodes:
            if not issubclass(node, ast.AST):
                raise ValueError(f"expected ast.AST subclass got: {node}")
            else:
                key = node.__name__.lower()
                if key in Evalable._NODES_HANDLERS:
                    raise ValueError(f"already got handler for {key}")
                func = classdict.get(key)
                if func is None:
                    raise ValueError(f"class {cls} does not implement handler for {key}")
                raise isinstance(func, classmethod) or ValueError(f"func {func} is not a classmethod of class {cls}")
            new_handlers.append(key)

        cls_ = super().__new__(cls, name, bases, classdict)
        for handler in new_handlers:
            Evalable._NODES_HANDLERS[handler] = getattr(cls_, handler)

        return cls_