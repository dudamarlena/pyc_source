# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_essentials/lib/mount_utils_prerequisites.py
# Compiled at: 2015-02-02 00:03:59
import pm_utils
skip_apt_update_default = False

def mount_prerequisites(skip_apt_update=skip_apt_update_default):
    """Checks whether necessary packages for mounting have been installed and installs them if necessary using `pm_utils.install_packages`. Returns `True` if packages were installed and `False`otherwise."""
    installed = False
    if not pm_utils.dpkg_check_package_installed('nfs-common'):
        pm_utils.install_packages(['nfs-common'], skip_apt_update=skip_apt_update)
        installed = True
    if not pm_utils.dpkg_check_package_installed('cifs-utils'):
        pm_utils.install_packages(['cifs-utils'], skip_apt_update=skip_apt_update)
        installed = True
    return installed