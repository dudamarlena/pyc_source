# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rulebox\__init__.py
# Compiled at: 2010-12-21 14:32:55
"""
A package containing various sets of rules for use with SUIT.

-----------------------------
Example Usage
-----------------------------

::

    import suit # easy_install suit
    from rulebox import templating
    template = open('template.tpl').read()
    # Template contains "Hello, <strong>[var]username[/var]</strong>!"
    templating.var.username = 'Brandon'
    print suit.execute(templating.rules, template)
    # Result: Hello, <strong>Brandon</strong>!

Basic usage; see http://www.suitframework.com/docs/ for other uses.
"""
__version__ = '1.1.1'