# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/__init__.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 635 bytes
"""
prompt_tool_kit
==============

Author: Jonathan Slenders

Description: prompt_tool_kit is a Library for building powerful interactive
             command lines in Python.  It can be a replacement for GNU
             readline, but it can be much more than that.

See the examples directory to learn about the usage.

Probably, to get started, you meight also want to have a look at
`prompt_tool_kit.shortcuts.prompt`.
"""
from .interface import CommandLineInterface
from .application import AbortAction, Application
from .shortcuts import prompt, prompt_async
__version__ = '1.0.14'