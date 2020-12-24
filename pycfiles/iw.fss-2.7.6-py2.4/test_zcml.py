# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/tests/test_zcml.py
# Compiled at: 2008-10-23 05:55:15
"""
Testing the ZCML meta and associated modules
"""
__author__ = ''
__docformat__ = 'restructuredtext'
import unittest
from zope.testing import doctest
from zope.testing.doctest import ELLIPSIS

def test_typewithfss():
    """
    Test fss:typeWithFSS directive::

        >>> from Products.Five import zcml
        >>> import iw.fss
        >>> template = '''
        ... <configure
        ...   xmlns="http://namespaces.zope.org/zope"
        ...   xmlns:fss="http://namespaces.ingeniweb.com/filesystemstorage">
        ...   %s
        ... </configure>'''
        >>> zcml.load_config('meta.zcml', iw.fss)

    Existing product configuration::

        >>> atfile_directive = '''
        ... <fss:typeWithFSS
        ...   class="Products.ATContentTypes.atct.ATFile"
        ...   fields="file" />'''
        >>> config_zcml = template % atfile_directive
        >>> zcml.load_string(config_zcml)

    Make sure we configured it::

        >>> from Products.ATContentTypes.atct import ATFile
        >>> ATFile.schema['file'].storage
        <Storage FileSystemStorage>

    The patched type has been registered::

        >>> from iw.fss.zcml import patchedTypesRegistry
        >>> len(patchedTypesRegistry)
        1
        >>> patchedTypesRegistry[ATFile]
        {u'file': <Storage AnnotationStorage>}

    Not existing content type or class::

        >>> stupid_directive = '''
        ... <fss:typeWithFSS
        ...   class="no.such.class"
        ...   fields="woof" />'''
        >>> config_zcml = template % stupid_directive
        >>> zcml.load_string(config_zcml)
        Traceback (most recent call last):
        ...
        ZopeXMLConfigurationError: ...

    Class is not Archetypes content type::

        >>> stupid_directive = '''
        ... <fss:typeWithFSS
        ...   class="smtplib.SMTP"
        ...   fields="woof" />'''
        >>> config_zcml = template % stupid_directive
        >>> zcml.load_string(config_zcml)
        Traceback (most recent call last):
        ...
        ConfigurationExecutionError: exceptions.AttributeError: class SMTP has no attribute 'schema'
        ...

    No such field in valid content type::

        >>> stupid_directive = '''
        ... <fss:typeWithFSS
        ...   class="Products.ATContentTypes.atct.ATFile"
        ...   fields="file nosuchfield" />'''
        >>> config_zcml = template % stupid_directive
        >>> zcml.load_string(config_zcml)
        Traceback (most recent call last):
        ...
        ConfigurationExecutionError: exceptions.KeyError: u'nosuchfield'
        ...
    """
    pass


def test_suite():
    return unittest.TestSuite((doctest.DocTestSuite(optionflags=ELLIPSIS),))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')