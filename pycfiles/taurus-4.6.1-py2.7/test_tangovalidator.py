# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/tango/test/test_tangovalidator.py
# Compiled at: 2019-08-19 15:09:29
"""Test for taurus.core.tango.test.test_tangovalidator..."""
__docformat__ = 'restructuredtext'
import unittest
from taurus.core.test import valid, invalid, names, AbstractNameValidatorTestCase
from taurus.core.tango.tangovalidator import TangoAuthorityNameValidator, TangoDeviceNameValidator, TangoAttributeNameValidator
import PyTango, socket
__PY_TANGO_HOST = PyTango.ApiUtil.get_env_var('TANGO_HOST')
host, port = __PY_TANGO_HOST.split(':')
__TANGO_HOST = ('{0}:{1}').format(socket.getfqdn(host), port)

@valid(name='tango://foo:10000')
@invalid(name='tango:foo')
@invalid(name='tango:foo:10000')
@invalid(name='tango://foo:10000/')
@invalid(name='tango://foo:10000/?')
@invalid(name='tango://foo:bar')
@invalid(name='tango://foo:10000/foo')
@names(name='tango://foo:123', out=('tango://foo:123', '//foo:123', 'foo:123'))
@names(name='//foo:123', out=('tango://foo:123', '//foo:123', 'foo:123'))
class TangoAuthValidatorTestCase(AbstractNameValidatorTestCase, unittest.TestCase):
    validator = TangoAuthorityNameValidator


@valid(name='tango:foo', groups={'devname': 'foo', '_devalias': 'foo', 
   '_devslashname': None})
@valid(name='tango:a/b/c', groups={'devname': 'a/b/c', '_devalias': None, 
   '_devslashname': 'a/b/c'})
@valid(name='tango://foo:123/a/b/c', groups={'devname': 'a/b/c', '_devalias': None, 
   '_devslashname': 'a/b/c'})
@valid(name='tango:a/b/ c', groups={'devname': 'a/b/ c'})
@invalid(name='tango:/a/b/c?')
@valid(name='tango://a/b/c', strict=False)
@valid(name='tango:alias')
@valid(name='tango://alias', strict=False)
@valid(name='tango://a/b/c', strict=False)
@invalid(name='tango:foo:1234/alias', strict=False)
@invalid(name='tango:foo:1234/a/b/c', strict=False)
@valid(name='foo:1234/alias', strict=False)
@valid(name='foo:1234/a/b/c', strict=False)
@invalid(name='tango://a/b/c', strict=True)
@invalid(name='tango://devalias')
@names(name='tango://foo:123/a/b/c', out=('tango://foo:123/a/b/c', '//foo:123/a/b/c',
                                          'a/b/c'))
@names(name='tango:sys/tg_test/1', out=(
 'tango://%s/sys/tg_test/1' % __TANGO_HOST,
 'sys/tg_test/1', 'sys/tg_test/1'))
@names(name='tango:alias', out=(None, None, 'alias'))
class TangoDevValidatorTestCase(AbstractNameValidatorTestCase, unittest.TestCase):
    validator = TangoDeviceNameValidator


@valid(name='foo:10000/a/b/c/d', strict=False)
@valid(name='mot/position', strict=False)
@valid(name='tango:a/b/c/d', groups={'devname': 'a/b/c', 'attrname': 'a/b/c/d', 
   '_shortattrname': 'd'})
@valid(name='tango:alias/attr', groups={'devname': 'alias', '_devalias': 'alias', 
   'attrname': 'alias/attr', 
   '_shortattrname': 'attr'})
@valid(name='tango://a/b/c/d', strict=False)
@valid(name='tango://alias/attr', strict=False)
@invalid(name='tango://a/b/c/d')
@invalid(name='tango://a/b/c/')
@invalid(name='tango://alias/attr')
@invalid(name='tango://a/b/c/d?')
@invalid(name='tango:a/b/c')
@invalid(name='tango:sys/tg_test/1')
@names(name='tango://foo:123/a/b/c/d', out=('tango://foo:123/a/b/c/d', '//foo:123/a/b/c/d',
                                            'd'))
@names(name='tango:sys/tg_test/1/float_scalar', out=(
 'tango://%s/sys/tg_test/1/float_scalar' % __TANGO_HOST,
 'sys/tg_test/1/float_scalar', 'float_scalar'))
@valid(name='tango:a/b/c/d#', groups={'devname': 'a/b/c', 'attrname': 'a/b/c/d', '_shortattrname': 'd', 'cfgkey': ''})
@valid(name='tango:a/b/c/d#label', groups={'devname': 'a/b/c', 'attrname': 'a/b/c/d', '_shortattrname': 'd', 'cfgkey': 'label'})
@valid(name='tango:alias/attr#')
@valid(name='tango:alias/attr#label')
@valid(name='tango://a/b/c/d?configuration', strict=False)
@valid(name='tango://a/b/c/d?configuration=label', strict=False, groups={'devname': 'a/b/c', 'attrname': 'a/b/c/d', 
   '_shortattrname': 'd', 
   'cfgkey': 'label', 
   'fragment': 'label'})
@invalid(name='tango://a/b/c/d#')
@invalid(name='tango://a/b/c/d?foo', strict=False)
@invalid(name='tango://a/b/c/d?foo=label', strict=False)
@valid(name='tango:a/b/c/d#?foo=label')
@valid(name='tango:a/b/c/d#label?foo=bar')
@names(name='tango://foo:123/a/b/c/d#', out=('tango://foo:123/a/b/c/d', '//foo:123/a/b/c/d',
                                             'd', ''))
@names(name='tango://foo:123/a/b/c/d#label', out=('tango://foo:123/a/b/c/d', '//foo:123/a/b/c/d',
                                                  'd', 'label'))
@names(name='tango:sys/tg_test/1/float_scalar#', out=(
 'tango://%s/sys/tg_test/1/float_scalar' % __TANGO_HOST,
 'sys/tg_test/1/float_scalar', 'float_scalar', ''))
@names(name='tango://foo:123/a/b/c/d?configuration=label', out=('tango://foo:123/a/b/c/d',
                                                                '//foo:123/a/b/c/d',
                                                                'd', 'label'))
class TangoAttrValidatorTestCase(AbstractNameValidatorTestCase, unittest.TestCase):
    validator = TangoAttributeNameValidator


if __name__ == '__main__':
    pass