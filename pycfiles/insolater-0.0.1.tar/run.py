# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/david/python/insolater/insolater/run.py
# Compiled at: 2013-11-02 19:50:03
import argparse
from insolater import Insolater

def cli(inso, argv):
    help_str = ('{cmd} init [<remote_changes>]\t\tstarts a new session.\n' + '{cmd} pwd\t\t\t\tdisplays current version.\n' + '{cmd} cd <ORIG or CHANGES>\t\tswitches to the requested version\n' + '{cmd} pull <remote_changes>\t\tpulls remote changes branch\n' + '{cmd} push <remote_location>\t\tpulls remote changes branch\n' + '{cmd} exit [<remote_changes>]\t\tends the session.').format(cmd=Insolater._CMD)
    if len(argv) == 0 or argv[0] == '-h' or argv[0] == '--help':
        print help_str
        return
    try:
        if argv[0] == 'init':
            if len(argv) <= 2:
                print inso.init(*argv[1:])
            else:
                print ('Usage: {cmd} init [remote_changes]').format(cmd=Insolater._CMD)
        elif argv[0] == 'pull':
            if len(argv) == 2:
                print inso.pull(argv[1])
            else:
                print ('Usage: {cmd} pull <remote_changes>').format(cmd=Insolater._CMD)
        elif argv[0] == 'push':
            if len(argv) == 2:
                print inso.push(argv[1])
            else:
                print ('Usage: {cmd} push <remote_changes>').format(cmd=Insolater._CMD)
        elif argv[0] == 'pwd':
            head = inso.get_current_branch()
            if head == 'CHANGES':
                print 'Currently in CHANGES version.'
            else:
                print 'Currently in ORIG version.'
        elif argv[0] == 'cd':
            if len(argv) < 2:
                print ('Usage: {cmd} cd <ORIG or CHANGES>').format(cmd=Insolater._CMD)
            else:
                print inso.change_branch(argv[1])
        elif argv[0] == 'exit':
            if len(argv) <= 2:
                print inso.exit(*argv[1:])
            else:
                print ('Usage: {cmd} exit [<remote_changes>]').format(cmd=Insolater._CMD)
        else:
            print ("Not a {cmd} command. See '{cmd} --help'.").format(cmd=Insolater._CMD)
    except Exception as error_msg:
        print error_msg.message


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--timeout', type=int, default=5, help='set timeout for file transfers')
    parser.add_argument('-r', '--repo', type=str, default='.insolater_repo', help='set repository to store CHANGES and ORIG')
    parser.add_argument('-p', '--filepattern', type=str, default='. *.py *.txt *.xml', help='set repository to store CHANGES and ORIG')
    parser.add_argument('cmd', nargs='+', help='command')
    args = parser.parse_args()
    i = Insolater(repo=args.repo, timeout=args.timeout, filepattern=args.filepattern)
    cli(i, args.cmd)


if __name__ == '__main__':
    main()