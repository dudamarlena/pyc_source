# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/__init__.py
# Compiled at: 2016-06-13 19:21:50
"""
:mod:`vsm` -- Cloud IaaS Platform
===================================

.. automodule:: vsm
   :platform: Unix
   :synopsis: Infrastructure-as-a-Service Cloud platform.
.. moduleauthor:: Jesse Andrews <jesse@ansolabs.com>
.. moduleauthor:: Devin Carlen <devin.carlen@gmail.com>
.. moduleauthor:: Vishvananda Ishaya <vishvananda@gmail.com>
.. moduleauthor:: Joshua McKenty <joshua@cognition.ca>
.. moduleauthor:: Manish Singh <yosh@gimp.org>
.. moduleauthor:: Andy Smith <andy@anarkystic.com>
"""
import gettext, sys, pkg_resources

def replace_dist(requirement):
    try:
        return pkg_resources.require(requirement)
    except pkg_resources.VersionConflict:
        e = sys.exc_info()[1]
        dist = e.args[0]
        req = e.args[1]
        if dist.key == req.key and not dist.location.endswith('.egg'):
            del pkg_resources.working_set.by_key[dist.key]
            return pkg_resources.require(requirement)


replace_dist('WebOb >= 1.0')
replace_dist('SQLAlchemy >= 0.6.3')
replace_dist('Routes >= 1.12.3')
replace_dist('PasteDeploy >= 1.5.0')
import paste
paste.__path__.insert(0, paste.__path__.pop(-1))
gettext.install('vsm', unicode=1)