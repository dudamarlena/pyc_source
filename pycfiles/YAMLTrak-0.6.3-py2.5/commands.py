# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/yamltrak/commands.py
# Compiled at: 2009-04-18 21:09:37
import os, textwrap
from termcolor import colored
from yamltrak.argparse import ArgumentParser
from yamltrak import IssueDB, NoRepository, NoIssueDB

def guess_issue_id(issuedb):
    related = issuedb.related(detail=True)
    if len(related) > 1:
        print colored('Too many linked issues found, please specify one.', None, attrs=['reverse'])
        for issueid in related:
            print colored(textwrap.fill('Issue: %s' % issueid, initial_indent='    ', subsequent_indent='    '), None, attrs=[])
            print colored(textwrap.fill(related[issueid].get('title', '').upper(), initial_indent='    ', subsequent_indent='    '), None, attrs=[])

        import sys
        sys.exit(1)
    issueid = related.keys()[0]
    print 'Found only one issue.'
    print colored(textwrap.fill('Issue: %s' % issueid, initial_indent='    ', subsequent_indent='    '), None, attrs=[])
    print colored(textwrap.fill(related[issueid].get('title', '').upper(), initial_indent='    ', subsequent_indent='    '), None, attrs=[])
    verification = raw_input('Do you want to use this issue? (Y/[N]) ')
    if verification.lower() in ('y', 'yes', 'yeah', 'oui', 'uh-huh', 'sure', 'why not?',
                                'meh'):
        return issueid
    print 'Aborting'
    import sys
    sys.exit(1)
    return


def unpack_new(issuedb, args):
    skeleton_new = issuedb.skeleton_new
    issue = {}
    for field in skeleton_new:
        issue[field] = getattr(args, field, None)
        if issue[field] is None:
            issue[field] = skeleton_new[field]

    newid = issuedb.new(issue=issue)
    print 'Added new issue: %s' % newid
    return


def unpack_list(issuedb, args):
    issues = issuedb.issues(status=args.status)
    for (id, issue) in issues.iteritems():
        color = None
        if 'high' in issue.get('priority', ''):
            color = 'red'
        elif 'normal' in issue.get('priority', ''):
            pass
        elif 'low' in issue.get('priority', ''):
            color = 'blue'
        else:
            color = 'red'
        if 'long' in issue.get('estimate', {}).get('scale').lower():
            indent = '>>>>'
        elif 'medium' in issue.get('estimate', {}).get('scale').lower():
            indent = '> > '
        elif 'short' in issue.get('estimate', {}).get('scale').lower():
            indent = '>   '
        else:
            indent = '===='
        print colored('Issue: %s' % id, color, attrs=['reverse'])
        print colored(textwrap.fill(issue.get('title', '').upper(), initial_indent=indent, subsequent_indent=indent), color, attrs=[])
        print colored(textwrap.fill(issue.get('estimate', {}).get('text', ''), initial_indent=indent, subsequent_indent=indent), color)

    return


def unpack_edit(issuedb, args):
    if not args.id:
        args.id = guess_issue_id(issuedb)
    skeleton = issuedb.skeleton
    issue = issuedb.issue(id=args.id, detail=False)[0]['data']
    newissue = {}
    for field in skeleton:
        newissue[field] = getattr(args, field, None) or issue.get(field, skeleton[field])

    issuedb.edit(id=args.id, issue=newissue)
    return


def unpack_show(issuedb, args):
    if not args.id:
        args.id = guess_issue_id(issuedb)
    issuedata = issuedb.issue(id=args.id, detail=args.detail)
    if not issuedata or not issuedata[0].get('data'):
        print 'No such issue found'
        return
    issue = issuedata[0]['data']
    print '\nIssue: %s' % args.id
    if 'title' in issue:
        print textwrap.fill(issue.get('title', '').upper(), initial_indent='', subsequent_indent='')
    if 'description' in issue:
        print textwrap.fill(issue['description'], initial_indent='', subsequent_indent='')
    print ''
    for field in sorted(issue.keys()):
        if field in ('title', 'description'):
            continue
        print textwrap.fill('%s: %s' % (field.upper(), issue[field]), initial_indent='', subsequent_indent='  ')

    if issue.get('diff'):
        for changeset in issue['diff'][0].iteritems():
            print 'Added: %s - %s' % (changeset[0].upper(), changeset[1])

        for changeset in issue['diff'][1].iteritems():
            print 'Removed: %s' % changeset[0].upper()

        for changeset in issue['diff'][2].iteritems():
            print 'Changed: %s - %s' % (changeset[0].upper(), changeset[1][1])

    for version in issuedata[1:]:
        print '\nChangeset: %s' % version['node']
        print 'Committed by: %s on %s' % (version['user'], version['date'])
        print 'Linked files:'
        for filename in version['files']:
            print '    %s' % filename

        if version.get('diff'):
            for changeset in version['diff'][0].iteritems():
                print 'Added: %s - %s' % (changeset[0].upper(), changeset[1])

            for changeset in version['diff'][1].iteritems():
                print 'Removed: %s' % changeset[0].upper()

            for changeset in version['diff'][2].iteritems():
                print 'Changed: %s - %s' % (changeset[0].upper(), changeset[1][1])


def unpack_related(issuedb, args):
    relatedissues = issuedb.related(filenames=args.files, detail=True)
    for (issueid, issue) in relatedissues.iteritems():
        print colored(textwrap.fill('Issue: %s' % issueid, initial_indent='    ', subsequent_indent='    '), None, attrs=[])
        print colored(textwrap.fill(issue.get('title', '').upper(), initial_indent='    ', subsequent_indent='    '), None, attrs=[])

    return


def unpack_dbinit(issuedb, args):
    try:
        issuedb = IssueDB(args.repository, dbinit=True)
    except NoRepository:
        print 'Unable to find a repository.'
        import sys
        sys.exit(1)
    except NoIssueDB:
        print 'Error initializing issued database'
        import sys
        sys.exit(1)

    print 'Initialized issue database'


def unpack_close(issuedb, args):
    if not args.id:
        args.id = guess_issue_id(issuedb)
    issuedb.close(args.id, args.comment)


def unpack_purge(issuedb, args):
    pass


def unpack_burndown(issuedb, args):
    pass


def main():
    """Parse the command line options and react to them."""
    try:
        issuedb = IssueDB(os.getcwd())
    except NoRepository:
        print 'Unable to find a repository.'
        import sys
        sys.exit(1)
    except NoIssueDB:
        parser = ArgumentParser(prog='yt', description='YAMLTrak is a distributed version controlled issue tracker.')
        subparsers = parser.add_subparsers(help=None, dest='command')
        parser_dbinit = subparsers.add_parser('dbinit', help='Initialize the issue database.')
        parser_dbinit.set_defaults(func=unpack_dbinit)
        args = parser.parse_args()
        args.repository = os.getcwd()
        args.func(None, args)
        return

    skeleton = issuedb.skeleton
    skeleton_new = issuedb.skeleton_new
    parser = ArgumentParser(prog='yt', description='YAMLTrak is a distributed version controlled issue tracker.')
    subparsers = parser.add_subparsers(help=None, dest='command')
    parser_new = subparsers.add_parser('new', help='Add a new issue.')
    parser_new.set_defaults(func=unpack_new)
    for (field, help) in skeleton.iteritems():
        if field not in skeleton_new:
            parser_new.add_argument('-' + field[0], '--' + field, help=help)

    for (field, help) in skeleton_new.iteritems():
        parser_new.add_argument('-' + field[0], '--' + field, required=True, help=skeleton[field])

    parser_edit = subparsers.add_parser('edit', help='Edit an issue.')
    parser_edit.set_defaults(func=unpack_edit)
    for (field, help) in skeleton.iteritems():
        parser_edit.add_argument('-' + field[0], '--' + field, help=help)

    parser_edit.add_argument('id', nargs='?', help='The issue id to edit.')
    parser_list = subparsers.add_parser('list', help='List all issues.')
    parser_list.set_defaults(func=unpack_list)
    parser_list.add_argument('-s', '--status', default='open', help='List all issues with this stats.  Defaults to open issues.')
    parser_show = subparsers.add_parser('show', help='Show the details for an issue.')
    parser_show.set_defaults(func=unpack_show)
    parser_show.add_argument('-d', '--detail', default=False, action='store_true', help='Show a detailed view of the issue')
    parser_show.add_argument('id', nargs='?', help='The issue id to show the details for.')
    parser_related = subparsers.add_parser('related', help='List the issues related to given files.')
    parser_related.set_defaults(func=unpack_related)
    parser_related.add_argument('files', metavar='file', type=str, nargs='*', default=[], help='List the open issues related to these files.  If no files are supplied, and the list of currently uncommitted files (excluding issues) will be checked.')
    parser_dbinit = subparsers.add_parser('dbinit', help='Initialize the issue database.')
    parser_dbinit.set_defaults(func=unpack_dbinit)
    parser_close = subparsers.add_parser('close', help='Close an issue.')
    parser_close.add_argument('-c', '--comment', default=None, help='An optional closing comment to set on the ticket.')
    parser_close.set_defaults(func=unpack_close)
    parser_close.add_argument('id', nargs='?', help='The issue id to close.')
    args = parser.parse_args()
    args.func(issuedb, args)
    return


if __name__ == '__main__':
    main()