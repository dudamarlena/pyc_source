# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-fat/egg/schevoweb/helper.py
# Compiled at: 2006-09-08 16:55:59
"""Schevo web helpers.

For copyright, license, and warranty, see bottom of file.
"""
import elementtree.ElementTree as etree
from schevo import base
from schevo.label import label
from schevoweb.form import fill, form_template
__all__ = [
 'fill', 'fix_tags', 'form_template', 'method_link', 'method_links', 'query_link', 'query_links', 'transaction_link', 'transaction_links', 'view_link', 'view_links']
MAGIC = '****$$%%--REMOVE--%%$$****'

def fix_tags(tree):
    """Return a string version of ``elem``, turning <textarea/> tags
    into <textarea></textarea> and <select/> into <select></select>."""
    for tag in tree.getiterator('textarea'):
        if tag.text == '':
            tag.text = MAGIC

    for tag in tree.getiterator('select'):
        if not tag.getchildren():
            tag.text = MAGIC

    s = etree.tostring(tree).replace('>%s</textarea>' % MAGIC, '></textarea>')
    return s


def method_link(obj, ns_name, name, action, linkto_fn, url_fn):
    """Return a link to a method.

    - ``obj``: The Schevo object to get the method from.

    - ``ns_name``: The namespace name on ``obj`` to get the method
      from.

    - ``name``: The name of the method to return a link for.

    - ``action``: The action to pass to ``url_fn``.

    - ``linkto_fn``: A callable that returns the actual link, that has
      the signature ``linkto_fn(text, url)``.

    - ``url_fn``: A callable that returns an URL based on keyword
      arguments.  The keyword arguments that are passed are
      ``action``, ``name``, ``extent_name``, and ``id``.  The ``id``
      argument may be `None`.
    """
    if isinstance(obj, base.Extent):
        extent_name = obj.name
        oid = None
    else:
        extent_name = obj.sys.extent.name
        oid = obj.sys.oid
    namespace = getattr(obj, ns_name)
    method = getattr(namespace, name)
    q_label = label(method)
    url = url_fn(action=action, name=name, extent_name=extent_name, id=oid)
    return linkto_fn(q_label, url)


def method_links(obj, ns_name, action, linkto_fn, url_fn):
    """Return a list of links to methods, sorted by method name.

    - ``obj``: The Schevo object to get methods from.

    - ``ns_name``: The namespace name on ``obj`` to get methods.

    - ``action``: The action to pass to ``url_fn``.

    - ``linkto_fn``: A callable that returns the actual link, that has
      the signature ``linkto_fn(text, url)``.

    - ``url_fn``: A callable that returns an URL based on keyword
      arguments.  The keyword arguments that are passed are
      ``action``, ``name``, ``extent_name``, and ``id``.  The ``id``
      argument may be `None`.
    """
    namespace = getattr(obj, ns_name)
    return [ method_link(obj, ns_name, name, action, linkto_fn, url_fn) for name in sorted(namespace) ]


def query_link(obj, name, linkto_fn, url_fn):
    return method_link(obj, 'q', name, 'new_query', linkto_fn, url_fn)


def query_links(obj, linkto_fn, url_fn):
    return method_links(obj, 'q', 'new_query', linkto_fn, url_fn)


def transaction_link(obj, name, linkto_fn, url_fn):
    return method_link(obj, 't', name, 'new_transaction', linkto_fn, url_fn)


def transaction_links(obj, linkto_fn, url_fn):
    return method_links(obj, 't', 'new_transaction', linkto_fn, url_fn)


def view_link(obj, name, linkto_fn, url_fn):
    return method_link(obj, 'v', name, 'view', linkto_fn, url_fn)


def view_links(obj, linkto_fn, url_fn):
    return method_links(obj, 'v', 'view', linkto_fn, url_fn)