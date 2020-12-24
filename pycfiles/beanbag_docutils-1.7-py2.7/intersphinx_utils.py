# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/beanbag_docutils/sphinx/ext/intersphinx_utils.py
# Compiled at: 2018-06-14 23:50:40
"""Sphinx extension to enhance intersphinx support.

This fixes some reference issues with :rst:role:`option` (see
https://github.com/sphinx-doc/sphinx/pull/3769 for the equivalent upstream
fix).

It also introduces a ``.. default-intersphinx::`` directive that allows for
specifying one or more intersphinx set prefixes that should be tried if a
reference could not be found. For example::

    .. default-intersphinx:: myapp1.5 python

    :ref:`some-reference`

This does affect the process by which missing references are located. If an
unprefixed reference is used, it will only match if the prefix is in the list
above, which differs from the default behavior of looking through all
intersphinx mappings.

Setup
=====

This extension must be added to ``exetnsions`` in :file:`conf.py` after the
:py:mod:`sphinx.ext.intersphinx` extension is added. For example::

    extensions = [
        ...
        'sphinx.ext.intersphinx',
        'beanbag_docutils.sphinx.ext.intersphinx',
        ...
    ]
"""
from __future__ import unicode_literals
import re, six
from docutils.parsers.rst import Directive
from sphinx.errors import ExtensionError
from sphinx.ext import intersphinx

class DefaultIntersphinx(Directive):
    """Specifies one or more default intersphinx sets to use."""
    required_arguments = 1
    optional_arguments = 100
    SPLIT_RE = re.compile(b',\\s*')

    def run(self):
        """Run the directive.

        Returns:
            list:
            An empty list, always.
        """
        env = self.state.document.settings.env
        env.metadata[env.docname][b'default-intersphinx-prefixes'] = self.arguments
        return []


def _on_missing_reference(app, env, node, contnode):
    """Handler for missing references.

    This will attempt to fix references to options and then attempt to
    apply default intersphinx prefixes (if needed) before resolving a
    reference using intersphinx.

    Args:
        app (sphinx.application.Sphinx):
            The Sphinx application processing the document.

        env (sphinx.environment.BuildEnvironment):
            The environment for this doc build.

        node (sphinx.addnodes.pending_xref):
            The pending reference to resolve.

        contnode (docutils.nodes.literal):
            The context for the reference.

    Returns:
        list:
        The list of any reference nodes, as created by intersphinx.
    """
    orig_target = node[b'reftarget']
    target = orig_target
    domain = node.get(b'refdomain')
    if domain == b'std' and node[b'reftype'] == b'option':
        i = target.rfind(b' ')
        if i != -1:
            target = b'%s.%s' % (target[:i], target[i + 1:])
            target = target.replace(b' ', b'-')
        else:
            progname = node.get(b'std:program')
            if progname:
                if b':' in target:
                    setname, newtarget = target.split(b':', 1)
                    target = b'%s:%s.%s' % (setname, progname, newtarget)
                else:
                    target = b'%s.%s' % (progname, target)
    if b':' not in target:
        prefixes = env.metadata[env.docname].get(b'default-intersphinx-prefixes')
        if prefixes:
            for prefix in prefixes:
                old_content = contnode[0]
                node[b'reftarget'] = b'%s:%s' % (prefix, target)
                result = intersphinx.missing_reference(app, env, node, contnode)
                if result:
                    return result
                node[b'reftarget'] = orig_target
                contnode[0] = old_content

            return None
    return intersphinx.missing_reference(app, env, node, contnode)


def setup(app):
    """Set up the Sphinx extension.

    This listens for the events needed to handle missing references, and
    registers directives.

    Args:
        app (sphinx.application.Sphinx):
            The Sphinx application building the docs.
    """
    app.add_directive(b'default-intersphinx', DefaultIntersphinx)
    listeners = app.events.listeners.get(b'missing-reference', {})
    for listener_id, callback in six.iteritems(listeners):
        if callback == intersphinx.missing_reference:
            del listeners[listener_id]
            break
    else:
        raise ExtensionError(b'beanbag_docutils.sphinx.ext.intersphinx_utils must come after sphinx.ext.intersphinx')

    app.connect(b'missing-reference', _on_missing_reference)