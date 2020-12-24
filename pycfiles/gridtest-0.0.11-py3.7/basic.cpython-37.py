# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/modules/basic.py
# Compiled at: 2020-04-23 17:36:49
# Size of source mod 2**32: 656 bytes


def add(one, two):
    """add will add two numbers, one and two. There is no typing here"""
    return one + two


def add_with_type(one: int, two: int) -> int:
    """add_with_type will add two numbers, one and two, with typing for ints."""
    return one + two


def hello(name):
    """print hello to a name, with no typing"""
    print(f"hello {name}!")


def hello_with_default(name='Dinosaur'):
    """print hello to a name with a default"""
    print(f"hello {name}!")


def hello_with_type(name: str) -> None:
    """print hello to a name, with typing"""
    print(f"hello {name}!")