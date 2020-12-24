# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\index\lib\dump_html.py
# Compiled at: 2013-09-15 13:30:49
from __future__ import division, absolute_import, print_function, unicode_literals
import logging
from inspect import ismethod
from xml.sax.saxutils import escape, prepare_input_source
from .backwardcompat import *

def plain_val(obj):
    if obj is None:
        buf = b'/is None/'
    elif isinstance(obj, numeric_types):
        buf = unicode(obj)
    else:
        try:
            buf = unicode(obj)
        except:
            buf = repr(obj)
            buf = buf.replace(b'\\n', b'\n')
            buf = buf.replace(b'\\r', b'')

    return buf


def plain(obj):
    buf = b'\n'
    buf += b'Iter свойства:\n==============\n'
    list_buf = b''
    if not isinstance(obj, string_types):
        try:
            for val in obj:
                list_buf += (b'{0}\n').format(plain_val(val))

        except:
            pass

    if list_buf:
        buf += list_buf
    buf += b'\n'
    buf += b'Dict свойства:\n==============\n'
    list_buf = b''
    if not isinstance(obj, string_types):
        try:
            for key, val in obj.items():
                list_buf += (b'{0:20}: {1}\n').format(key, plain_val(val))

        except:
            pass

    if list_buf:
        buf += list_buf
    buf += b'\n'
    buf += b'dict свойства:\n==============\n'
    if hasattr(obj, b'__dict__'):
        d = obj.__dict__
        for key in sorted(d.keys()):
            if key[0:2] != b'__':
                val = d.get(key)
                buf += (b'{0:20}: {1}\n').format(key, plain_val(val))

    buf += b'\n'
    buf += b'dir свойства:\n=============\n'
    dirs_buf = b''
    for key in dir(obj):
        val = getattr(obj, key)
        if not callable(val):
            if key[0:2] != b'__':
                dirs_buf += (b'{0:20}: {1}\n').format(key, plain_val(val))

    if dirs_buf:
        buf += dirs_buf
    buf += b'\n'
    buf += b'Callable свойства:\n==================\n'
    dirs_buf = b''
    for key in dir(obj):
        val = getattr(obj, key)
        if callable(val):
            if key[0:2] != b'__':
                dirs_buf += (b'{0:20}: {1}\n').format(key, plain_val(val))

    if dirs_buf:
        buf += dirs_buf
    buf += b'\n'
    return buf


def html_type(obj):
    return escape(plain_val(type(obj)))


def html_val(obj, color=b''):
    type_obj = html_type(obj)
    obj = escape(plain_val(obj))
    obj = obj.replace(b'\r\n', b'<br />')
    obj = obj.replace(b'\r', b'<br />')
    obj = obj.replace(b'\n', b'<br />')
    if color:
        buf = (b'<span title="{0}" style="color: {1}">{2}</span>').format(type_obj, color, obj)
    else:
        buf = (b'<span title="{0}">{1}</span>').format(type_obj, obj)
    return buf


def html(obj, it=1, root=None, collection=[]):
    if root is None:
        collection = []
    if root is obj:
        return b'<span style="color: red"><i>on self</i></span>'
    else:
        buf = b''
        if obj is None:
            buf = b'<span style="color: Gray"><i>is None</i></span>'
        else:
            if isinstance(obj, numeric_types):
                buf = html_val(obj, b'blue')
            else:
                if isinstance(obj, simple_types):
                    buf = html_val(obj)
                if buf:
                    return buf
            for i in collection:
                if i is obj:
                    return html_val(obj, b'red')

        collection.append(obj)
        if isinstance(obj, (list, tuple)):
            buf = b'<ul>\n'
            for value in obj:
                buf += (b'<li>{0}</li>').format(html(value, it, obj, collection))

            buf += b'</ul>\n'
        else:
            if isinstance(obj, dict):
                buf = b'<ul>\n'
                for key, value in obj.items():
                    buf += (b'<li>{0}: {1}</li>').format(key, html(value, it, obj, collection))

                buf += b'</ul>\n'
            if buf:
                return buf
            if not it:
                return html_val(obj, b'Dimgray')
        it -= 1
        buf = html_r(obj, it, root, collection)
        return buf


def html_r(obj, it=1, root=None, collection=[]):
    buf = b'<table border="1">\n'
    buf += (b'  <tr><th colspan="2" style="background-color: Cornflowerblue">{0}</th></tr>\n').format(html_val(obj))
    dirs_buf = b''
    for key in dir(obj):
        val = getattr(obj, key)
        if not ismethod(val):
            if key[0:2] != b'__':
                dirs_buf += (b'  <tr><td style="color: blue"><b>{0}</b></td><td>{1}</td></tr>\n').format(key, html(val, it, obj, collection))

    if dirs_buf:
        buf += dirs_buf
    buf += b'</table>\n'
    return buf