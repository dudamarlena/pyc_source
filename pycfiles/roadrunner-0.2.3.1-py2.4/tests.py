# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/roadrunner/tests.py
# Compiled at: 2009-06-16 00:05:39
import os, re, shutil, sys, zc.buildout.tests, zc.buildout.testing, unittest
from zope.testing import doctest, renormalizing
os_path_sep = os.path.sep
if os_path_sep == '\\':
    os_path_sep *= 2

def dirname(d, level=1):
    if level == 0:
        return d
    return dirname(os.path.dirname(d), level - 1)


def setUp(test):
    zc.buildout.tests.easy_install_SetUp(test)


def test_suite():
    globs = dict(plone_buildout_cfg=plone_buildout_cfg)
    suite = unittest.TestSuite((doctest.DocFileSuite('recipe.txt', setUp=setUp, tearDown=zc.buildout.testing.buildoutTearDown, globs=globs, checker=renormalizing.RENormalizing([zc.buildout.testing.normalize_path, zc.buildout.testing.normalize_script, zc.buildout.testing.normalize_egg_py, zc.buildout.tests.normalize_bang, (re.compile('zc.buildout(-\\S+)?[.]egg(-link)?'), 'roadrunner'), (re.compile('[-d]  setuptools-[^-]+-'), 'setuptools-X-')])),))
    return suite


plone_buildout_cfg = '[buildout]\nparts=\n#  zope2\n  plone\n  instance\n  roadrunner\ndevelop=\n  src/test_package\n  src/preloaded_package\n  %s/..\neggs =\n  elementtree\n  test_package\n  preloaded_package\n  roadrunner\neggs-directory=/Users/jbb/.buildout/eggs\ndownload-directory=/Users/jbb/.buildout/downloads\ndownload-cache=/Users/jbb/.buildout/download-cache\n\n[plone]\nrecipe = plone.recipe.plone\n\n[zope2]\n#recipe = plone.recipe.zope2install\n#url = ${plone:zope2-url}\nlocation=/Users/jbb/co/shared_plone3/parts/zope2\n\n[instance]\nrecipe = plone.recipe.zope2instance\nzope2-location = ${zope2:location}\nuser = admin:admin\nhttp-address = 8080\neggs =\n    ${buildout:eggs}\n    ${plone:eggs}\nproducts =\n#    /Users/jbb/co/shared_plone3/parts/plone\n    ${plone:products}\n\n[roadrunner]\nrecipe = roadrunner:plone\n#preload-packages = preloaded_package\npackage-under-test = test_package\n' % os.path.dirname(__file__)
if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')