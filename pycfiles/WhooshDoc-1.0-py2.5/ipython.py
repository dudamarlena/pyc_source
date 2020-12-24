# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/whooshdoc/ipython.py
# Compiled at: 2009-02-23 01:54:38
""" IPython extension for querying WhooshDoc indices.
"""
from __future__ import with_statement
from contextlib import contextmanager
from pydoc import resolve
import IPython.ipapi
from whooshdoc.search import ResultsMenu
from whooshdoc.util import create_or_open_index, default_index, query_help
ip = IPython.ipapi.get()

@contextmanager
def ipython_history_protect():
    """ Protect a block of code that uses raw_input() from interfering with
    IPython's history.
    """
    if ip.IP.has_readline:
        import IPython.rlineimpl as readline
        try:
            old_rl_length = readline.get_current_history_length()
            do_rl_fix = True
        except AttributeError:
            do_rl_fix = False

    yield
    if ip.IP.has_readline and do_rl_fix:
        new_rl_length = readline.get_current_history_length()
        for i in range(old_rl_length, new_rl_length)[::-1]:
            readline.remove_history_item(i)


@contextmanager
def always_page():
    """ Temporarily monkeypatch IPython.OInspect.page() to always page
    regardless of the size of the screen.
    """
    from IPython import OInspect
    old_page = OInspect.page

    def safe_page(strng, start=0, screen_lines=0, pager_cmd=None):
        old_page(strng, start=start, screen_lines=1, pager_cmd=pager_cmd)

    OInspect.page = safe_page
    yield
    OInspect.page = old_page
    return


class IPythonResultsMenu(ResultsMenu):
    """ Results menu using IPython's help? mechanism.
    """

    def help(self, name):
        """ Overridden to use IPython's mechanism.
        """
        name = str(name)
        (obj, junk) = resolve(name)
        with always_page():
            ip.IP.shell.inspector.pinfo(obj, name)


def magic_whoosh(self, parameter_s=''):
    """ Search the docstring index for functions, classes, methods, and modules.

    %whoosh <search terms>

    A numbered list of search results will be shown paginated with an input
    prompt. At the prompt, the user can type the number of result to see its
    pydoc help.
    """
    if not hasattr(ip, 'whoosh_index'):
        raise IPython.ipapi.UsageError('Whoosh index has not been defined.')
    query_string = unicode(parameter_s)
    with ipython_history_protect():
        rm = IPythonResultsMenu.query(ip.whoosh_index, query_string, funcs_first=True)
        rm.mainloop()


magic_whoosh.__doc__ += query_help

def enable(indexname=None):
    """ Enable this extension with the given index filename.
    """
    if indexname is None:
        indexname = default_index()
    ip.whoosh_index = create_or_open_index(indexname)
    ip.expose_magic('whoosh', magic_whoosh)
    return