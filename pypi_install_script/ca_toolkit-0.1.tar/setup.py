# -*- coding: utf-8 -*-
from setuptools import setup, Extension


modules = [
    Extension('ca_toolkit.evolve', ['src/mod_evolve.c', 'src/evolve.c']),
]

setup(
    name='ca_toolkit',
    version='0.1',
    description='Python toolkit for Cellular Automata',
    author="Tong Zhang",
    author_email="warriorlance@gmail.com",
    url="https://github.com/archman/ca-toolkit.git",
    ext_modules=modules,
    packages=['ca_toolkit'],
    install_requires=['matplotlib', 'numpy'],
)
