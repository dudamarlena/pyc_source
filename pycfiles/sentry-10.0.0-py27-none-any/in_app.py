# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/in_app.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import re
IOS_APP_PATHS = ('/var/containers/Bundle/Application/', '/private/var/containers/Bundle/Application/')
MACOS_APP_PATHS = ('.app/Contents/', '/Users/', '/usr/local/')
LINUX_SYS_PATHS = ('/lib/', '/usr/lib/', 'linux-gate.so')
WINDOWS_SYS_PATH_RE = re.compile('^[a-z]:\\\\windows', re.IGNORECASE)
SUPPORT_FRAMEWORK_RE = re.compile('(?x)\n    /Frameworks/(\n            libswift([a-zA-Z0-9]+)\\.dylib$\n        |   (KSCrash|SentrySwift|Sentry)\\.framework/\n    )\n    ')

def _is_support_framework(package):
    return SUPPORT_FRAMEWORK_RE.search(package) is not None


def is_known_third_party(package, sdk_info=None):
    """
    Checks whether this package matches one of the well-known system image
    locations across platforms. The given package must not be ``None``.
    """
    if _is_support_framework(package):
        return True
    else:
        if package.startswith(IOS_APP_PATHS):
            return False
        if '/Developer/CoreSimulator/Devices/' in package and '/Containers/Bundle/Application/' in package:
            return False
        sdk_name = sdk_info['sdk_name'].lower() if sdk_info else ''
        if sdk_name == 'macos':
            return not any(p in package for p in MACOS_APP_PATHS)
        if sdk_name == 'linux':
            return package.startswith(LINUX_SYS_PATHS)
        if sdk_name == 'windows':
            return WINDOWS_SYS_PATH_RE.match(package) is not None
        return True


def is_optional_package(package, sdk_info=None):
    """
    Determines whether the given package is considered optional.

    This indicates that no error should be emitted if this package is missing
    during symbolication. Also, reprocessing should not block for this image.
    """
    if not package:
        return True
    if _is_support_framework(package):
        return True
    if package.startswith(IOS_APP_PATHS) and '/Frameworks/' in package:
        return True
    return False