# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/__init__.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 635 bytes
__doc__ = '\nprompt_tool_kit\n==============\n\nAuthor: Jonathan Slenders\n\nDescription: prompt_tool_kit is a Library for building powerful interactive\n             command lines in Python.  It can be a replacement for GNU\n             readline, but it can be much more than that.\n\nSee the examples directory to learn about the usage.\n\nProbably, to get started, you meight also want to have a look at\n`prompt_tool_kit.shortcuts.prompt`.\n'
from .interface import CommandLineInterface
from .application import AbortAction, Application
from .shortcuts import prompt, prompt_async
__version__ = '1.0.14'