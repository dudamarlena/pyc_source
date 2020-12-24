# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/common/version.py
# Compiled at: 2011-09-28 13:50:09
__all__ = 'get_git_version'
from subprocess import Popen, PIPE

def call_git_describe(abbrev=4):
    try:
        p = Popen(['git', 'describe', '--abbrev=%d' % abbrev], stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readlines()[0]
        return line.strip()
    except:
        return

    return


def read_release_version():
    try:
        f = open('RELEASE-VERSION', 'r')
        try:
            version = f.readlines()[0]
            return version.strip()
        finally:
            f.close()

    except:
        return

    return


def write_release_version(version):
    f = open('RELEASE-VERSION', 'w')
    f.write('%s\n' % version)
    f.close()


def strip_version_tag_decorations(text):
    """
    We're using a naming convention where each version tag in the
    repository starts from `v` letter, so we have to remove it to obtain
    a standard version string (starting from a number)
    """
    if text[0] == 'v' and text[1] in [ str(i) for i in xrange(10) ]:
        return text[1:]
    return text


def get_git_version(abbrev=4):
    release_version = read_release_version()
    version = call_git_describe(abbrev)
    if version is None:
        version = release_version
    if version is None:
        raise ValueError('Cannot find the version number!')
    if version != release_version:
        write_release_version(version)
    stripped_version = strip_version_tag_decorations(version)
    return stripped_version


if __name__ == '__main__':
    print get_git_version()