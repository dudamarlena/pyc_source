# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/PROGETTI/saxix/django-whatsnew/whatsnew/util.py
# Compiled at: 2014-04-04 16:23:02
import pkg_resources

def get_version(package_name):
    version = None
    try:
        version = pkg_resources.require(package_name)[0].version
    except pkg_resources.DistributionNotFound:
        module = __import__(package_name)
        try:
            func = getattr(module, 'get_version')
            version = func()
        except:
            for attempt in ('version', 'VERSION', '__version__'):
                try:
                    version = getattr(module, attempt)
                    if isinstance(version, (list, tuple)):
                        version = ('.').join(version)
                except AttributeError:
                    pass

    if version:
        return str(version)
    else:
        raise pkg_resources.DistributionNotFound
        return