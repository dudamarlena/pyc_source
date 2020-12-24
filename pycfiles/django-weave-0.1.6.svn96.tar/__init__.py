# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jens/workspace/django-weave/django_weave_env/src/django-weave/testproject/__init__.py
# Compiled at: 2010-04-06 10:18:39
"""
    Check some external libs with pkg_resources.require()
    We only create warnings on VersionConflict and DistributionNotFound exceptions.
    
    See also: ./scripts/requirements/external_apps.txt
    See also: ./scripts/requirements/libs.txt
    
    Format info for pkg_resources.require():
    http://peak.telecommunity.com/DevCenter/PkgResources#requirement-objects
"""
import warnings, pkg_resources

def check_require(requirements):
    """
    Check a package list.
    Display only warnings on VersionConflict and DistributionNotFound exceptions.
    """
    for requirement in requirements:
        try:
            pkg_resources.require(requirement)
        except pkg_resources.VersionConflict, err:
            warnings.warn('Version conflict: %s' % err)
        except pkg_resources.DistributionNotFound, err:
            warnings.warn('Distribution not found: %s' % err)


requirements = ('django >= 1.1', )
check_require(requirements)