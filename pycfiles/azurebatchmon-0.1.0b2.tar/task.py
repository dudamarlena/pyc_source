# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kchiba/azurebatchmon/azurebatchmon/task.py
# Compiled at: 2018-02-28 22:15:23
import sys, os

class Task:

    def __init__(self):
        self.env = {}
        self.inputs = {}
        self.input_recursive = {}
        self.outputs = {}
        self.output_recursive = {}