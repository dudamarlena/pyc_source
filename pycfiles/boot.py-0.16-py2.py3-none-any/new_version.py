# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/fabrizio/Dropbox/free_range_factory/boot/boot_pkg/new_version.py
# Compiled at: 2012-08-07 08:52:49
import xmlrpclib, pip
from pkg_resources import parse_version

def check_on_pypi():
    """ Check for new versions of "boot" on the Pypi server.
        This function returns only text lines.
    """
    import argparse
    parser = argparse.ArgumentParser(description='Program to compile, simulate and synthesize ' + 'your VHDL code.', epilog='Program made by: freerangefactory.org')
    parser.add_argument('-l', '--log', required=False, dest='log', action='store_const', const=True, default=False, help='Start boot and log output into a local file.')
    parser.add_argument('-m', '--mirror', dest='mirror', default='http://pypi.python.org/pypi')
    args = parser.parse_args()
    pypi = xmlrpclib.ServerProxy(args.mirror)
    for local in pip.get_installed_distributions():
        if local.project_name == 'boot':
            try:
                available = pypi.package_releases(local.project_name)
            except:
                return 'Problems in checking the pypi server. ' + 'Maybe the connection is down.'

            if available:
                comparison = cmp(parse_version(available[0]), parse_version(local.version))
                print 'Installed version:', local.version
                print 'Version available for download:', available[0]
                if comparison == 0:
                    return 'Current version of "boot" is ' + local.version + ' and it is the newest version.'
                if comparison < 0:
                    return 'Pypi server has an older version of "boot".'
                return 'A newer version (ver. ' + available[0] + ') of boot is available for download.\n' + 'Run the terminal command:' + ' "sudo pip install --upgrade boot" and restart boot.'
            else:
                return 'No package named "boot" is found on pypi servers.'

    return 'No package named "boot" installed in your machine.\n' + 'Run the terminal command: sudo pip install boot'