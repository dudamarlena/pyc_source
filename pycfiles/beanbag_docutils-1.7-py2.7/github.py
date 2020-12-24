# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/beanbag_docutils/sphinx/ext/github.py
# Compiled at: 2018-06-14 23:50:40
"""Sphinx extension to link to source code on GitHub.

This links to source code for modules, classes, etc. to the correct line on
GitHub. This prevents having to bundle the source code along with the
documentation, and better ties everything together.

Setup
=====

To use this, you'll need to import the module and define your own
:py:func:`linkcode_resolve` in your :file:`conf.py`::

    from beanbag_docutils.sphinx.ext.github import github_linkcode_resolve

    extensions = [
        ...
        'sphinx.ext.linkcode',
        ...
    ]

    def linkcode_resolve(domain, info):
        return github_linkcode_resolve(
            domain=domain,
            info=info,
            allowed_module_names=['mymodule'],
            github_org_id='myorg',
            github_repo_id='myrepo',
            branch='master',
            source_prefix='src/')

``source_prefix`` and ``allowed_module_names`` are optional. See the
docs for :py:func:`github_linkcode_resolve` for more information.
"""
from __future__ import unicode_literals
import inspect, re, subprocess, sys
GIT_BRANCH_CONTAINS_RE = re.compile(b'^\\s*([^\\s]+)\\s+([0-9a-f]+)\\s.*')
_head_ref = None

def _run_git(cmd):
    """Run git with the given arguments, returning the output.

    Args:
        cmd (list of unicode):
            A list of arguments to pass to :command:`git`.

    Returns:
        str:
        The resulting output from the command.

    Raises:
        subprocess.CalledProcessError:
            Error calling into git.
    """
    p = subprocess.Popen([b'git'] + cmd, stdout=subprocess.PIPE)
    output, error = p.communicate()
    ret_code = p.poll()
    if ret_code:
        raise subprocess.CalledProcessError(ret_code, b'git')
    return output


def _git_get_nearest_tracking_branch(merge_base, remote=b'origin'):
    """Return the nearest tracking branch for the given Git repository.

    Args:
        merge_base (unicode):
            The merge base used to locate the nearest tracking branch.

        remote (origin, optional):
            The remote name.

    Returns:
        unicode:
        The nearest tracking branch, or ``None`` if not found.
    """
    try:
        _run_git([b'fetch', b'origin', b'%s:%s' % (merge_base, merge_base)])
    except Exception:
        pass

    lines = _run_git([b'branch', b'-rv', b'--contains', merge_base]).splitlines()
    remote_prefix = b'%s/' % remote
    best_distance = None
    best_ref_name = None
    for line in lines:
        m = GIT_BRANCH_CONTAINS_RE.match(line.decode(b'utf-8').strip())
        if m:
            ref_name = m.group(1)
            sha = m.group(2)
            if ref_name.startswith(remote_prefix) and not ref_name.endswith(b'/HEAD'):
                distance = len(_run_git([b'log',
                 b'--pretty=format:%%H',
                 b'...%s' % sha]).splitlines())
                if best_distance is None or distance < best_distance:
                    best_distance = distance
                    best_ref_name = ref_name

    if best_ref_name and best_ref_name.startswith(remote_prefix):
        best_ref_name = best_ref_name[len(remote_prefix):]
    return best_ref_name


def _get_git_doc_ref(branch):
    """Return the commit SHA used for linking to source code on GitHub.

    The commit SHA will be cached for future lookups.

    Args:
        branch (unicode):
            The branch to use as a merge base.

    Returns:
        unicode:
        The commit SHA used for any links, if found, or ``None`` if not.
    """
    global _head_ref
    if not _head_ref:
        try:
            tracking_branch = _git_get_nearest_tracking_branch(branch)
            _head_ref = _run_git([b'rev-parse', tracking_branch]).strip()
        except subprocess.CalledProcessError:
            _head_ref = None

    return _head_ref


def github_linkcode_resolve(domain, info, github_org_id, github_repo_id, branch, source_prefix=b'', allowed_module_names=[]):
    """Return a link to the source on GitHub for the given autodoc info.

    This takes some basic information on the GitHub project, branch, and
    what modules are considered acceptable, and generates a link to the
    approprite line on the GitHub repository browser for the class, function,
    variable, or other object.

    Args:
        domain (unicode):
            The autodoc domain being processed. This only accepts "py", and
            comes from the original :py:func:`linkcode_resolve` call.

        info (dict):
            Information on the item being linked to. This comes from the
            original :py:func:`linkcode_resolve` call.

        github_org_id (unicode):
            The GitHub organization ID.

        github_repo_id (unicode):
            The GitHub repository ID.

        branch (unicode):
            The branch used as a merge base to find the appropriate commit
            to link to. Callers may want to compute this off of the version
            number of the project, or some other information.

        source_prefix (unicode, optional):
            A prefix for any linked filename, in case the module is not at
            the top of the source tree.

        allowed_module_names (list of unicode, optional):
            The list of top-level module names considered valid for links.
            If provided, links will only be generated if residing somewhere
            in one of the provided module names.
    """
    module_name = info[b'module']
    if domain != b'py' or not module_name or allowed_module_names and module_name.split(b'.')[0] not in allowed_module_names:
        return
    filename = module_name.replace(b'.', b'/') + b'.py'
    submod = sys.modules.get(module_name)
    if submod is None:
        return
    else:
        obj = submod
        for part in info[b'fullname'].split(b'.'):
            try:
                obj = getattr(obj, part)
            except:
                return

        try:
            linenum = inspect.findsource(obj)[1]
        except:
            linenum = None

        if linenum:
            linespec = b'#L%d' % (linenum + 1)
        else:
            linespec = b''
        ref = _get_git_doc_ref(branch) or branch
        return b'https://github.com/%s/%s/blob/%s/%s%s%s' % (
         github_org_id, github_repo_id, ref, source_prefix,
         filename, linespec)