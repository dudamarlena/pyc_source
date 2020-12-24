# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autoversion_pbr/__init__.py
# Compiled at: 2016-11-15 13:25:07
from __future__ import print_function
import errno, os, pbr.packaging, subprocess, sys
from packaging.version import Version, InvalidVersion
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser

def main():
    parser = ConfigParser()
    parser.readfp(open('setup.cfg'))
    cfg = {}
    for section in parser.sections():
        cfg[section] = dict(parser.items(section))

    try:
        ver = autoversion(cfg)
    except AutoVersionError as err:
        sys.exit(str(err))

    print(ver)


def autoversion(cfg):
    tag, branch, tags = git_info()
    if tag:
        return tag
    if not branch:
        raise AutoVersionError('Unable to generate a package version unless a branch is checked out in git.')
    buckets = get_version_buckets(cfg)
    tags_by_branch, tags_by_bucket = sort_tags(buckets, tags)
    if branch in tags_by_branch:
        reference_tag = max(tags_by_branch[branch])
    else:
        reference_tag = find_reference(branch, buckets, tags_by_bucket)
    delta = count_commits(branch, reference_tag)
    print(('autoversion: {} commits since reference point {}').format(delta, reference_tag), file=sys.stderr)
    if not delta:
        raise AutoVersionError(('Unable to generate version: no commits on branch {0} after reference {1}. Make sure {1} is merged into {0}').format(branch, reference_tag))
    return make_version(branch, buckets, reference_tag, delta)


def git_info():
    try:
        current_commit = subprocess.check_output([
         'git', 'rev-parse', 'HEAD']).decode('utf8').strip()
    except OSError as err:
        if err.args[0] == errno.ENOENT:
            raise AutoVersionError('Not a git checkout or git is not installed')
        raise

    current_tag = None
    tags = []
    for line in subprocess.check_output([
     'git', 'ls-remote', '.']).splitlines():
        commit, ref = line.decode('utf8').strip().split(None, 1)
        if not ref.startswith('refs/tags/'):
            continue
        if not ref.endswith('^{}'):
            continue
        tag = ref[10:-3]
        if 'dev' in tag:
            continue
        try:
            tag = Version(tag.strip())
        except InvalidVersion:
            continue

        tags.append(tag)
        if commit == current_commit:
            current_tag = tag

    branch = os.getenv('GIT_BRANCH')
    if branch:
        branch = branch.split('/')[(-1)]
    else:
        try:
            branch = subprocess.check_output([
             'git', 'symbolic-ref', '--short', 'HEAD'], stderr=open(os.devnull, 'wb')).decode('utf8').strip()
        except subprocess.CalledProcessError:
            branch = None

    return (
     current_tag, branch, tags)


def get_version_buckets(cfg):
    buckets = []
    for name, value in cfg['autoversion'].items():
        if not name.startswith('branches.'):
            continue
        branch = name[9:]
        versions = value.replace(',', ' ').split()
        for version in versions:
            buckets.append((Version(version), branch))

    buckets.sort(reverse=True)
    return buckets


def sort_tags(buckets, tags):
    tags_by_branch = {}
    tags_by_bucket = {}
    for tag in tags:
        for bucket, branch in buckets:
            if str(tag).startswith(str(bucket) + '.'):
                break
        else:
            continue

        tags_by_branch.setdefault(branch, []).append(tag)
        tags_by_bucket.setdefault(bucket, []).append(tag)

    for tags in tags_by_branch.values():
        tags.sort()

    for tags in tags_by_bucket.values():
        tags.sort()

    return (
     tags_by_branch, tags_by_bucket)


def find_reference(branch, buckets, tags_by_bucket):
    branch_buckets = [ ver for ver, x in buckets if x == branch ]
    if not branch_buckets:
        raise AutoVersionError(('Unable to generate a package version: no setting for branch {}').format(branch))
    branch_first_bucket = min(branch_buckets)
    preceding_buckets = [ ver for ver, x in buckets if ver < branch_first_bucket
                        ]
    if not preceding_buckets:
        return
    else:
        best_preceding_bucket = max(preceding_buckets)
        tags = tags_by_bucket.get(best_preceding_bucket, ())
        if tags:
            return min(tags)
        return
        return


def count_commits(branch, reference):
    if reference:
        ids = subprocess.check_output([
         'git', 'rev-list', '--ancestry-path',
         ('{}..{}').format(reference, branch)])
    else:
        ids = subprocess.check_output(['git', 'rev-list', '--all'])
    return ids.count('\n')


def make_version(branch, buckets, reference, delta):
    base = max(ver for ver, x in buckets if x == branch)
    if reference and reference >= base:
        base, patchlevel = reference.base_version.rsplit('.', 1)
        patchlevel = int(patchlevel) + 1
    else:
        base = str(base)
        patchlevel = 0
    ver = Version(('{}.{}.dev{}').format(base, patchlevel, delta))
    assert reference and ver > reference
    return ver


class AutoVersionError(RuntimeError):
    pass


def hook(cfg):

    def _patched_getver(pre_version=None):
        try:
            return str(autoversion(cfg))
        except AutoVersionError as err:
            print(('autoversion failed: {}').format(str(err)), file=sys.stderr)
            return ''

    pbr.packaging._get_version_from_git = _patched_getver
    return


def distutils_keyword(dist, attr, value):
    pass


if __name__ == '__main__':
    main()