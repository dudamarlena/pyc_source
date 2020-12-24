# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jessemaitland/PycharmProjects/commando/venv/lib/python3.6/site-packages/rambo/mapper/mapper.py
# Compiled at: 2019-09-25 01:52:54
# Size of source mod 2**32: 554 bytes


def get_function_names(config: dict) -> list:
    actions = config['commands']['action']['choices']
    objects = config['commands']['object']['choices']
    return [f"{a}_{o}" for a in actions for o in objects]


def function_mapper(config: dict, modules: list) -> dict:
    mapped_functions = {}
    functions = get_function_names(config)
    for module in modules:
        for function in functions:
            func = getattr(module, function, None)
            if func:
                mapped_functions[function] = func

    return mapped_functions