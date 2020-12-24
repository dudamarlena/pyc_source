# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwharry/lscsoft_git/src/pycbc-glue/misc/generate_vcs_info.py
# Compiled at: 2017-03-10 08:37:44
__author__ = 'Adam Mercer <adam.mercer@ligo.org>'
import exceptions, os, sys, time, optparse, filecmp, shutil
try:
    import subprocess
except ImportError:
    sys.exit('Python-2.4, or higher is required')

class git_info(object):

    def __init__(self):
        id = None
        date = None
        branch = None
        tag = None
        author = None
        committer = None
        status = None
        return


class GitInvocationError(exceptions.LookupError):
    pass


def parse_args():
    usage = '%prog [options] project src_dir build_dir'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('--sed', action='store_true', default=False, help='output sed commands for version replacement')
    parser.add_option('--sed-file', action='store_true', default=False, help='output sed file for version replacement')
    opts, args = parser.parse_args()
    if len(args) != 3:
        parser.error('incorrect number of command line options specified')
    if opts.sed and opts.sed_file:
        parser.error('cannot specify both --sed and --sed-file')
    return (opts, args[0], args[1], args[2])


def call_out(command):
    """
  Run the given command (with shell=False) and return a tuple of
  (int returncode, str output). Strip the output of enclosing whitespace.
  """
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, _ = p.communicate()
    return (
     p.returncode, out.strip())


def check_call_out(command):
    """
  Run the given command (with shell=False) and return the output as a
  string. Strip the output of enclosing whitespace.
  If the return code is non-zero, throw GitInvocationError.
  """
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, _ = p.communicate()
    if p.returncode != 0:
        raise GitInvocationError, 'failed to run "%s"' % (' ').join(command)
    return out.strip()


def in_git_repository():
    """
  Return True if git is available and we are in a git repository; else
  return False.

  NB: Unfortunately there is a magic number without any documentation to back
  it up. It turns out that git status returns non-zero exit codes for all sorts
  of success conditions, but I cannot find any documentation of them. 128 was
  determined empirically. I sure hope that it's portable.
  """
    ret_code, git_path = call_out(('which', 'git'))
    return ret_code != 1 and not git_path.startswith('no') and call_out((git_path, 'status'))[0] != 128


def generate_git_version_info():
    info = git_info()
    git_path = check_call_out(('which', 'git'))
    git_id, git_udate, git_author_name, git_author_email, git_committer_name, git_committer_email = check_call_out((git_path, 'log', '-1',
     '--pretty=format:%H,%ct,%an,%ae,%cn,%ce')).split(',')
    git_date = time.strftime('%Y-%m-%d %H:%M:%S +0000', time.gmtime(float(git_udate)))
    git_author = '%s <%s>' % (git_author_name, git_author_email)
    git_committer = '%s <%s>' % (git_committer_name, git_committer_email)
    branch_match = check_call_out((git_path, 'rev-parse',
     '--symbolic-full-name', 'HEAD'))
    if branch_match == 'HEAD':
        git_branch = None
    else:
        git_branch = os.path.basename(branch_match)
    status, git_tag = call_out((git_path, 'describe', '--exact-match',
     '--tags', git_id))
    if status != 0:
        git_tag = None
    check_call_out((git_path, 'update-index', '-q', '--refresh'))
    status_output = subprocess.call((git_path, 'diff-files', '--quiet'))
    if status_output != 0:
        git_status = 'UNCLEAN: Modified working tree'
    else:
        status_output = subprocess.call((git_path, 'diff-index', '--cached',
         '--quiet', 'HEAD'))
        if status_output != 0:
            git_status = 'UNCLEAN: Modified index'
        else:
            git_status = 'CLEAN: All modifications committed'
    info.id = git_id
    info.date = git_date
    info.branch = git_branch
    info.tag = git_tag
    info.author = git_author
    info.committer = git_committer
    info.status = git_status
    return info


if __name__ == '__main__':
    options, project, src_dir, build_dir = parse_args()
    basename = '%sVCSInfo.h' % project
    infile = '%s.in' % basename
    tmpfile = '%s/%s.tmp' % (build_dir, basename)
    srcfile = '%s/%s' % (src_dir, basename)
    dstfile = '%s/%s' % (build_dir, basename)
    if os.access(srcfile, os.F_OK) and not os.access(dstfile, os.F_OK):
        shutil.copy(srcfile, dstfile)
    os.chdir(src_dir)
    try:
        info = generate_git_version_info()
    except GitInvocationError:
        if not in_git_repository():
            sys.exit(0)
        else:
            sys.exit('Unexpected failure in discovering the git version')

    if options.sed_file:
        print 's/@ID@/%s/g' % info.id
        print 's/@DATE@/%s/g' % info.date
        print 's/@BRANCH@/%s/g' % info.branch
        print 's/@TAG@/%s/g' % info.tag
        print 's/@AUTHOR@/%s/g' % info.author
        print 's/@COMMITTER@/%s/g' % info.committer
        print 's/@STATUS@/%s/g' % info.status
    elif options.sed:
        sed_cmd = ('sed',
         '-e', 's/@ID@/%s/' % info.id,
         '-e', 's/@DATE@/%s/' % info.date,
         '-e', 's/@BRANCH@/%s/' % info.branch,
         '-e', 's/@TAG@/%s/' % info.tag,
         '-e', 's/@AUTHOR@/%s/' % info.author,
         '-e', 's/@COMMITTER@/%s/' % info.committer,
         '-e', 's/@STATUS@/%s/' % info.status,
         infile)
        sed_retcode = subprocess.call(sed_cmd, stdout=open(tmpfile, 'w'))
        if sed_retcode:
            raise GitInvocationError, 'Failed call (modulo quoting): ' + (' ').join(sed_cmd) + ' > ' + tmpfile
        if os.access(dstfile, os.F_OK) and filecmp.cmp(dstfile, tmpfile):
            os.remove(tmpfile)
        else:
            os.rename(tmpfile, dstfile)
    else:
        print 'Id: %s' % info.id
        print 'Date: %s' % info.date
        print 'Branch: %s' % info.branch
        print 'Tag: %s' % info.tag
        print 'Author: %s' % info.author
        print 'Committer: %s' % info.committer
        print 'Status: %s' % info.status