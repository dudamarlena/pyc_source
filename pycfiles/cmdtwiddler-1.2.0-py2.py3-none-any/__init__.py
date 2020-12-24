# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/side-project/lib/python2.7/site-packages/cmdtree/__init__.py
# Compiled at: 2016-08-28 23:20:32
from cmdtree.parser import AParser
from cmdtree.registry import env
from cmdtree.shortcuts import argument, option, command, group
from cmdtree.types import STRING, INT, FLOAT, BOOL, UUID, Choices, IntRange, File
env.parser = AParser()
entry = env.entry