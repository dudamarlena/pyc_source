# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pytest_diffeo/namespace.py
# Compiled at: 2016-04-08 13:51:41
"""Namespace support for Diffeo tests.

Many tests need a "namespace" string that defines part of a database,
work queue, or other persistent object.  This module defines a common
function `make_namespace_string` to create namespaces, and a py.test
`namespace_string` fixture to provide them.

-----

This software is released under an MIT/X11 open source license.

Copyright 2012-2014 Diffeo, Inc.

"""
from __future__ import absolute_import
import getpass, hashlib, os, re, socket, pytest

def make_namespace_string(test_name=''):
    """Generate a descriptive namespace for testing.

    The namespace string encodes the username, process ID, and host
    name of the running system.  The returned string is never longer
    than 40 characters, and never contains non-alphanumeric-underscore
    characters.  (It matches the regular expression
    [a-zA-Z0-9_]{,40}.)

    This is just a generated string!  If you use this, you are
    responsible for any application-defined semantics around creating
    and destroying the namespace.

    """
    s = ('_').join([
     re.sub('\\W', '', test_name)[-23:],
     getpass.getuser().replace('-', '_')[:5],
     str(os.getpid())[-5:],
     hashlib.md5(socket.gethostname()).hexdigest()[:4]])
    if s.startswith('_'):
        s = 'z' + s
    return s.lower()


@pytest.fixture(scope='function')
def namespace_string(request):
    """A dynamically namespace string.

    This is used by other fixtures to ensure that they use the same
    namespace.  If you use this directly, you are responsible for
    cleaning up the namespace when your test ends.  This can be reused
    by other components that have the notion of a "namespace".  Each
    individual test should have a distinct namespace.

    """
    return make_namespace_string(request.node.name)