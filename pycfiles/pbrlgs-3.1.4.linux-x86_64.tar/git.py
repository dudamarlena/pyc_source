# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pbr/git.py
# Compiled at: 2017-12-04 07:19:32
from __future__ import unicode_literals
import distutils.errors
from distutils import log
import errno, io, os, re, subprocess, time, pkg_resources
from pbr import options
from pbr import version

def _run_shell_command(cmd, throw_on_error=False, buffer=True, env=None):
    if buffer:
        out_location = subprocess.PIPE
        err_location = subprocess.PIPE
    else:
        out_location = None
        err_location = None
    newenv = os.environ.copy()
    if env:
        newenv.update(env)
    output = subprocess.Popen(cmd, stdout=out_location, stderr=err_location, env=newenv)
    out = output.communicate()
    if output.returncode and throw_on_error:
        raise distutils.errors.DistutilsError(b'%s returned %d' % (cmd, output.returncode))
    if len(out) == 0 or not out[0] or not out[0].strip():
        return b''
    return out[0].strip().decode(b'utf-8', b'replace')


def _run_git_command(cmd, git_dir, **kwargs):
    if not isinstance(cmd, (list, tuple)):
        cmd = [
         cmd]
    return _run_shell_command(([
     b'git', b'--git-dir=%s' % git_dir] + cmd), **kwargs)


def _get_git_directory():
    try:
        return _run_shell_command([b'git', b'rev-parse', b'--git-dir'])
    except OSError as e:
        if e.errno == errno.ENOENT:
            return b''
        raise


def _git_is_installed():
    try:
        _run_shell_command([b'git', b'--version'])
    except OSError:
        return False

    return True


def _get_highest_tag(tags):
    """Find the highest tag from a list.

    Pass in a list of tag strings and this will return the highest
    (latest) as sorted by the pkg_resources version parser.
    """
    return max(tags, key=pkg_resources.parse_version)


def _find_git_files(dirname=b'', git_dir=None):
    """Behave like a file finder entrypoint plugin.

    We don't actually use the entrypoints system for this because it runs
    at absurd times. We only want to do this when we are building an sdist.
    """
    file_list = []
    if git_dir is None:
        git_dir = _run_git_functions()
    if git_dir:
        log.info(b'[pbr] In git context, generating filelist from git')
        file_list = _run_git_command([b'ls-files', b'-z'], git_dir)
        file_list = file_list.split((b'\x00').decode(b'utf-8'))
    return [ f for f in file_list if f ]


def _get_raw_tag_info(git_dir):
    describe = _run_git_command([b'describe', b'--always'], git_dir)
    if b'-' in describe:
        return describe.rsplit(b'-', 2)[(-2)]
    else:
        if b'.' in describe:
            return 0
        return


def get_is_release(git_dir):
    return _get_raw_tag_info(git_dir) == 0


def _run_git_functions():
    git_dir = None
    if _git_is_installed():
        git_dir = _get_git_directory()
    return git_dir or None


def get_git_short_sha(git_dir=None):
    """Return the short sha for this repo, if it exists."""
    if not git_dir:
        git_dir = _run_git_functions()
    if git_dir:
        return _run_git_command([
         b'log', b'-n1', b'--pretty=format:%h'], git_dir)
    else:
        return


def _clean_changelog_message(msg):
    """Cleans any instances of invalid sphinx wording.

    This escapes/removes any instances of invalid characters
    that can be interpreted by sphinx as a warning or error
    when translating the Changelog into an HTML file for
    documentation building within projects.

    * Escapes '_' which is interpreted as a link
    * Escapes '*' which is interpreted as a new line
    * Escapes '`' which is interpreted as a literal
    """
    msg = msg.replace(b'*', b'\\*')
    msg = msg.replace(b'_', b'\\_')
    msg = msg.replace(b'`', b'\\`')
    return msg


def _iter_changelog(changelog):
    """Convert a oneline log iterator to formatted strings.

    :param changelog: An iterator of one line log entries like
        that given by _iter_log_oneline.
    :return: An iterator over (release, formatted changelog) tuples.
    """
    first_line = True
    current_release = None
    yield (current_release, b'CHANGES\n=======\n\n')
    for hash, tags, msg in changelog:
        if tags:
            current_release = _get_highest_tag(tags)
            underline = len(current_release) * b'-'
            if not first_line:
                yield (
                 current_release, b'\n')
            yield (
             current_release,
             b'%(tag)s\n%(underline)s\n\n' % dict(tag=current_release, underline=underline))
        if not msg.startswith(b'Merge '):
            if msg.endswith(b'.'):
                msg = msg[:-1]
            msg = _clean_changelog_message(msg)
            yield (current_release, b'* %(msg)s\n' % dict(msg=msg))
        first_line = False

    return


def _iter_log_oneline(git_dir=None):
    """Iterate over --oneline log entries if possible.

    This parses the output into a structured form but does not apply
    presentation logic to the output - making it suitable for different
    uses.

    :return: An iterator of (hash, tags_set, 1st_line) tuples, or None if
        changelog generation is disabled / not available.
    """
    if git_dir is None:
        git_dir = _get_git_directory()
    if not git_dir:
        return []
    else:
        return _iter_log_inner(git_dir)


def _is_valid_version(candidate):
    try:
        version.SemanticVersion.from_pip_string(candidate)
        return True
    except ValueError:
        return False


def _iter_log_inner(git_dir):
    """Iterate over --oneline log entries.

    This parses the output intro a structured form but does not apply
    presentation logic to the output - making it suitable for different
    uses.

    :return: An iterator of (hash, tags_set, 1st_line) tuples.
    """
    log.info(b'[pbr] Generating ChangeLog')
    log_cmd = [b'log', b'--decorate=full', b'--format=%h%x00%s%x00%d']
    changelog = _run_git_command(log_cmd, git_dir)
    for line in changelog.split(b'\n'):
        line_parts = line.split(b'\x00')
        if len(line_parts) != 3:
            continue
        sha, msg, refname = line_parts
        tags = set()
        if b'refs/tags/' in refname:
            refname = refname.strip()[1:-1]
            for tag_string in refname.split(b'refs/tags/')[1:]:
                candidate = tag_string.split(b', ')[0]
                if _is_valid_version(candidate):
                    tags.add(candidate)

        yield (
         sha, tags, msg)


def write_git_changelog(git_dir=None, dest_dir=os.path.curdir, option_dict=None, changelog=None):
    """Write a changelog based on the git changelog."""
    start = time.time()
    if not option_dict:
        option_dict = {}
    should_skip = options.get_boolean_option(option_dict, b'skip_changelog', b'SKIP_WRITE_GIT_CHANGELOG')
    if should_skip:
        return
    if not changelog:
        changelog = _iter_log_oneline(git_dir=git_dir)
        if changelog:
            changelog = _iter_changelog(changelog)
    if not changelog:
        return
    new_changelog = os.path.join(dest_dir, b'ChangeLog')
    if os.path.exists(new_changelog) and not os.access(new_changelog, os.W_OK):
        log.info(b'[pbr] ChangeLog not written (file already exists and it is not writeable)')
        return
    log.info(b'[pbr] Writing ChangeLog')
    with io.open(new_changelog, b'w', encoding=b'utf-8') as (changelog_file):
        for release, content in changelog:
            changelog_file.write(content)

    stop = time.time()
    log.info(b'[pbr] ChangeLog complete (%0.1fs)' % (stop - start))


def generate_authors(git_dir=None, dest_dir=b'.', option_dict=dict()):
    """Create AUTHORS file using git commits."""
    should_skip = options.get_boolean_option(option_dict, b'skip_authors', b'SKIP_GENERATE_AUTHORS')
    if should_skip:
        return
    else:
        start = time.time()
        old_authors = os.path.join(dest_dir, b'AUTHORS.in')
        new_authors = os.path.join(dest_dir, b'AUTHORS')
        if os.path.exists(new_authors) and not os.access(new_authors, os.W_OK):
            return
        log.info(b'[pbr] Generating AUTHORS')
        ignore_emails = b'(jenkins@review|infra@lists|jenkins@openstack)'
        if git_dir is None:
            git_dir = _get_git_directory()
        if git_dir:
            authors = []
            git_log_cmd = [
             b'log', b'--format=%aN <%aE>']
            authors += _run_git_command(git_log_cmd, git_dir).split(b'\n')
            authors = [ a for a in authors if not re.search(ignore_emails, a) ]
            co_authors_out = _run_git_command(b'log', git_dir)
            co_authors = re.findall(b'Co-authored-by:.+', co_authors_out, re.MULTILINE)
            co_authors = [ signed.split(b':', 1)[1].strip() for signed in co_authors if signed
                         ]
            authors += co_authors
            authors = sorted(set(authors))
            with open(new_authors, b'wb') as (new_authors_fh):
                if os.path.exists(old_authors):
                    with open(old_authors, b'rb') as (old_authors_fh):
                        new_authors_fh.write(old_authors_fh.read())
                new_authors_fh.write(((b'\n').join(authors) + b'\n').encode(b'utf-8'))
        stop = time.time()
        log.info(b'[pbr] AUTHORS complete (%0.1fs)' % (stop - start))
        return