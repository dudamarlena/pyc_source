# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/hooks/init/hook1.5/scripts/log-police.py
# Compiled at: 2010-09-24 12:39:25
import os, sys, getopt, svn, svn.fs, svn.repos, svn.core
try:
    True
except:
    True = 1
    False = 0

def fix_log_message(log_message):
    """Return a fixed version of LOG_MESSAGE.  By default, this just
  means ensuring that the result ends with exactly one newline and no
  other whitespace.  But if you want to do other kinds of fixups, this
  function is the place to implement them -- all log message fixing in
  this script happens here."""
    return log_message.rstrip() + '\n'


def fix_txn(fs, txn_name):
    """Fix up the log message for txn TXN_NAME in FS.  See fix_log_message()."""
    txn = svn.fs.svn_fs_open_txn(fs, txn_name)
    log_message = svn.fs.svn_fs_txn_prop(txn, 'svn:log')
    if log_message is not None:
        new_message = fix_log_message(log_message)
        if new_message != log_message:
            svn.fs.svn_fs_change_txn_prop(txn, 'svn:log', new_message)
    return


def fix_rev(fs, revnum):
    """Fix up the log message for revision REVNUM in FS.  See fix_log_message()."""
    log_message = svn.fs.svn_fs_revision_prop(fs, revnum, 'svn:log')
    if log_message is not None:
        new_message = fix_log_message(log_message)
        if new_message != log_message:
            svn.fs.svn_fs_change_rev_prop(fs, revnum, 'svn:log', new_message)
    return


def usage_and_exit(error_msg=None):
    """Write usage information and exit.  If ERROR_MSG is provide, that
  error message is printed first (to stderr), the usage info goes to
  stderr, and the script exits with a non-zero status.  Otherwise,
  usage info goes to stdout and the script exits with a zero status."""
    import os.path
    stream = error_msg and sys.stderr or sys.stdout
    if error_msg:
        stream.write('ERROR: %s\n\n' % error_msg)
    stream.write('USAGE: %s [-t TXN_NAME | -r REV_NUM | --all-revs] REPOS\n' % os.path.basename(sys.argv[0]))
    stream.write("\nEnsure that log messages end with exactly one newline and no other\nwhitespace characters.  Use as a pre-commit hook by passing '-t TXN_NAME';\nfix up a single revision by passing '-r REV_NUM'; fix up all revisions by\npassing '--all-revs'.  (When used as a pre-commit hook, may modify the\nsvn:log property on the txn.)\n")
    sys.exit(error_msg and 1 or 0)


def main(ignored_pool, argv):
    repos_path = None
    txn_name = None
    rev_name = None
    all_revs = False
    try:
        (opts, args) = getopt.getopt(argv[1:], 't:r:h?', ['help', 'all-revs'])
    except:
        usage_and_exit('problem processing arguments / options.')

    for (opt, value) in opts:
        if opt == '--help' or opt == '-h' or opt == '-?':
            usage_and_exit()
        elif opt == '-t':
            txn_name = value
        elif opt == '-r':
            rev_name = value
        elif opt == '--all-revs':
            all_revs = True
        else:
            usage_and_exit("unknown option '%s'." % opt)

    if txn_name is not None and rev_name is not None:
        usage_and_exit('cannot pass both -t and -r.')
    if txn_name is not None and all_revs:
        usage_and_exit('cannot pass --all-revs with -t.')
    if rev_name is not None and all_revs:
        usage_and_exit('cannot pass --all-revs with -r.')
    if rev_name is None and txn_name is None and not all_revs:
        usage_and_exit('must provide exactly one of -r, -t, or --all-revs.')
    if len(args) != 1:
        usage_and_exit('only one argument allowed (the repository).')
    repos_path = svn.core.svn_path_canonicalize(args[0])
    fs = svn.repos.svn_repos_fs(svn.repos.svn_repos_open(repos_path))
    if txn_name is not None:
        fix_txn(fs, txn_name)
    elif rev_name is not None:
        fix_rev(fs, int(rev_name))
    elif all_revs:
        last_youngest = 0
        while True:
            youngest = svn.fs.svn_fs_youngest_rev(fs)
            if youngest >= last_youngest:
                for this_rev in range(last_youngest, youngest + 1):
                    fix_rev(fs, this_rev)

                last_youngest = youngest + 1
            else:
                break

    return


if __name__ == '__main__':
    sys.exit(svn.core.run_app(main, sys.argv))