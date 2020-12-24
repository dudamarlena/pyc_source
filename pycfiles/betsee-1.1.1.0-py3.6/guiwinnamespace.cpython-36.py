# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/window/guiwinnamespace.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 2438 bytes
"""
Top-level classes defining this application's main window.

Motivation
----------
To avoid collisions between the names assigned by :mod:`PySide2`'s UI compiler
(UIC) to widget variables owned by the current :class:`QBetseeMainWindow`
instance, these names are typically prefixed or suffixed by common substrings
signifying ad-hoc namespaces. For example, all widgets with variable names
prefixed by :data:`SIM_CONF_STACK_PAGE_NAME_PREFIX` identify pages of the
top-level stack widget.

For maintainability, these prefixes and suffixes are centralized here rather
than chaotically dispersed throughout the codebase.
"""
SIM_CONF_STACK_PAGE_ITEMIZED_NAME_SUFFIX = '_item'
SIM_CONF_STACK_PAGE_NAME_PREFIX = 'sim_conf_stack_page_'