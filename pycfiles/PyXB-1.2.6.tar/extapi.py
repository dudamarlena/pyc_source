# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pyxbdist.WUiBAra/PyXB-1.2.6/doc/extapi.py
# Compiled at: 2017-09-03 07:16:21
from __future__ import print_function
import os.path
from docutils import nodes
import sys, re
__Reference_re = re.compile('\\s*(.*)\\s+<(.*)>\\s*$', re.MULTILINE + re.DOTALL)

def ticket_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Role `:ticket:` generates references to SourceForge tickets.
    """
    trac_root = 'https://sourceforge.net/p/pyxb/tickets'
    mo = __Reference_re.match(text)
    label = None
    if mo is not None:
        label, text = mo.group(1, 2)
    ticket = text.strip()
    uri = '%s/%s/' % (trac_root, ticket)
    if label is None:
        label = 'SF ticket %s' % (ticket,)
    node = nodes.reference(rawtext, label, refuri=uri, **options)
    return (
     [
      node], [])


def issue_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Role `:issue:` generates references to github issues.
    """
    issue_root = 'https://github.com/pabigot/pyxb/issues'
    mo = __Reference_re.match(text)
    label = None
    if mo is not None:
        label, text = mo.group(1, 2)
    ticket = text.strip()
    uri = '%s/%s/' % (issue_root, ticket)
    if label is None:
        label = 'issue %s' % (ticket,)
    node = nodes.reference(rawtext, label, refuri=uri, **options)
    return (
     [
      node], [])


def setup(app):
    app.add_role('ticket', ticket_role)
    app.add_role('issue', issue_role)