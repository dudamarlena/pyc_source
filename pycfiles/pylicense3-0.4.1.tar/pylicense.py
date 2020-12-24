# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/pylicense/pylicense.py
# Compiled at: 2013-02-03 07:28:23
__doc__ = " \nA script for extraction of the license metainformation from the python eggs in the specified folders.\nExpects the license information to be present in the distribution's metadata.\n\nBSD License\n\n(c) Ilja Livenson\n\n"
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