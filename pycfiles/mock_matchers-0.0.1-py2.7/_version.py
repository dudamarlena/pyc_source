# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/mock_matchers/_version.py
# Compiled at: 2014-09-02 08:59:56
git_refnames = '$Format:%d$'
git_full = '$Format:%H$'
import subprocess, sys

def run_command(args, cwd=None, verbose=False, hide_stderr=False):
    try:
        p = subprocess.Popen(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE if hide_stderr else None)
    except EnvironmentError:
        e = sys.exc_info()[1]
        if verbose:
            print 'unable to run %s' % args[0]
            print e
        return

    stdout = p.communicate()[0].strip()
    if sys.version >= '3':
        stdout = stdout.decode()
    if p.returncode != 0:
        if verbose:
            print 'unable to run %s (error)' % args[0]
        return
    return stdout


import sys, re, os.path

def get_expanded_variables(versionfile_abs):
    variables = {}
    try:
        f = open(versionfile_abs, 'r')
        for line in f.readlines():
            if line.strip().startswith('git_refnames ='):
                mo = re.search('=\\s*"(.*)"', line)
                if mo:
                    variables['refnames'] = mo.group(1)
            if line.strip().startswith('git_full ='):
                mo = re.search('=\\s*"(.*)"', line)
                if mo:
                    variables['full'] = mo.group(1)

        f.close()
    except EnvironmentError:
        pass

    return variables


def versions_from_expanded_variables(variables, tag_prefix, verbose=False):
    refnames = variables['refnames'].strip()
    if refnames.startswith('$Format'):
        if verbose:
            print 'variables are unexpanded, not using'
        return {}
    refs = set([ r.strip() for r in refnames.strip('()').split(',') ])
    TAG = 'tag: '
    tags = set([ r[len(TAG):] for r in refs if r.startswith(TAG) ])
    if not tags:
        tags = set([ r for r in refs if re.search('\\d', r) ])
        if verbose:
            print "discarding '%s', no digits" % (',').join(refs - tags)
    if verbose:
        print 'likely tags: %s' % (',').join(sorted(tags))
    for ref in sorted(tags):
        if ref.startswith(tag_prefix):
            r = ref[len(tag_prefix):]
            if verbose:
                print 'picking %s' % r
            return {'version': r, 'full': variables['full'].strip()}

    if verbose:
        print 'no suitable tags, using full revision id'
    return {'version': variables['full'].strip(), 'full': variables['full'].strip()}


def versions_from_vcs(tag_prefix, root, verbose=False):
    if not os.path.exists(os.path.join(root, '.git')):
        if verbose:
            print 'no .git in %s' % root
        return {}
    GIT = 'git'
    if sys.platform == 'win32':
        GIT = 'git.cmd'
    stdout = run_command([GIT, 'describe', '--tags', '--dirty', '--always'], cwd=root)
    if stdout is None:
        return {}
    else:
        if not stdout.startswith(tag_prefix):
            if verbose:
                print "tag '%s' doesn't start with prefix '%s'" % (stdout, tag_prefix)
            return {}
        tag = stdout[len(tag_prefix):]
        stdout = run_command([GIT, 'rev-parse', 'HEAD'], cwd=root)
        if stdout is None:
            return {}
        full = stdout.strip()
        if tag.endswith('-dirty'):
            full += '-dirty'
        return {'version': tag, 'full': full}


def versions_from_parentdir(parentdir_prefix, root, verbose=False):
    dirname = os.path.basename(root)
    if not dirname.startswith(parentdir_prefix):
        if verbose:
            print "guessing rootdir is '%s', but '%s' doesn't start with prefix '%s'" % (
             root, dirname, parentdir_prefix)
        return None
    return {'version': dirname[len(parentdir_prefix):], 'full': ''}


tag_prefix = ''
parentdir_prefix = 'mock_matchers-'
versionfile_source = 'mock_matchers/_version.py'

def get_versions(default={'version': 'unknown', 'full': ''}, verbose=False):
    variables = {'refnames': git_refnames, 'full': git_full}
    ver = versions_from_expanded_variables(variables, tag_prefix, verbose)
    if ver:
        return ver
    try:
        root = os.path.abspath(__file__)
        for i in range(len(versionfile_source.split('/'))):
            root = os.path.dirname(root)

    except NameError:
        return default

    return versions_from_vcs(tag_prefix, root, verbose) or versions_from_parentdir(parentdir_prefix, root, verbose) or default