# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/git_semver/main.py
# Compiled at: 2020-04-04 13:31:03
# Size of source mod 2**32: 1217 bytes
import argparse, os, sys
from git import Repo
from semantic_version import Version
from git_semver import get_current_version
from git_semver.constants import ERR_NO_VERSION_FOUND, ERR_NOT_A_REPO

def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--next-patch', '-p', dest='modifier', action='store_const', const=Version.next_patch)
    parser.add_argument('--next-minor', '-m', dest='modifier', action='store_const', const=Version.next_minor)
    parser.add_argument('--next-major', '-M', dest='modifier', action='store_const', const=Version.next_major)
    options = parser.parse_args(sys.argv[1:] if args is None else args)
    try:
        repo = Repo(os.getcwd())
    except:
        print('fatal: Not a git repository', file=sys.stderr)
        return ERR_NOT_A_REPO

    version = get_current_version(repo)
    if version is None:
        print('No version found. Try creating a tag with your initial version, for example:', file=sys.stderr)
        print('  git tag -am 0.1.0 0.1.0', file=sys.stderr)
        return ERR_NO_VERSION_FOUND
    if options.modifier:
        version = options.modifier(version)
    print(str(version).strip('-'))
    return 0