# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/pylicense/pylicense.py
# Compiled at: 2013-02-03 07:28:23
""" 
A script for extraction of the license metainformation from the python eggs in the specified folders.
Expects the license information to be present in the distribution's metadata.

BSD License

(c) Ilja Livenson

"""
import pkg_resources, argparse

def extract_license(egg_folder):
    for i in pkg_resources.find_distributions('eggs'):
        current_egg = '%s' % i
        current_egg_version = None
        for j in i._get_metadata('PKG-INFO'):
            if j.startswith('License:'):
                current_egg_version = j[9:]
                break

        print '%s, %s' % (current_egg, current_egg_version)

    return


parser = argparse.ArgumentParser(description='Extract license information from the egg files in specified folders.')
parser.add_argument('eggdirs', metavar='eggdir', type=str, nargs='+', help='A path containing python eggs')

def run():
    args = parser.parse_args()
    for eggdir in args.eggdirs:
        extract_license(eggdir)


if __name__ == '__main__':
    run()