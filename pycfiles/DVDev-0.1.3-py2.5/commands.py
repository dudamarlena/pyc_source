# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/dvdev/commands.py
# Compiled at: 2009-04-19 14:06:35
import os, sys, signal
from yamltrak.argparse import ArgumentParser
from mercurial import hg, ui, util, commands
from mercurial.error import RepoError

def build_repo_tree(root=os.getcwd(), maxdepth=2, firstrun=True):
    """Build a tree structure that represents the loaded repositories."""
    if maxdepth < 1 or not os.path.isdir(root):
        return
    if not firstrun:
        if '.hg' not in os.listdir(root):
            return [ build_repo_tree(subpath, maxdepth - 1, False) for subpath in os.listdir(root) ]
    myui = ui.ui()
    try:
        repo = hg.repository(myui, root)
    except (RepoError, util.Abort):
        return [ build_repo_tree(subpath, maxdepth - 1, False) for subpath in os.listdir(root) ]

    return os.path.abspath(root)


def flatten(lst):
    """    Temp function to flatten the nested lists. At some point, the repos will be
    in dictionaries that mirror the directory's tree structure."""
    output = []
    try:
        if not isinstance(lst, basestring):
            for elem in lst:
                output += flatten(elem)

        else:
            return [
             lst]
        return output
    except TypeError:
        return [
         lst]


def launch_and_watch_child(args):
    if hasattr(os, 'fork'):
        import webbrowser
        child = os.fork()
        if child == 0:
            return (
             None, child)
        (childpid, exit_code) = os.waitpid(child, 0)
        return (
         exit_code >> 8, child)
    from subprocess import Popen
    child = Popen(args)
    exit_code = child.wait()
    return (exit_code, child.pid)


def _server_args(args, nolaunch=False):
    if hasattr(os, 'fork'):
        args.fragile = True
        args.debug = False
        if nolaunch:
            args.nolaunch = True
        return
    import sys
    my_python = sys.executable
    if sys.platform == 'win32' and ' ' in my_python:
        my_python = my_python.replace(' ', '\\ ')
    server_args = [my_python] + sys.argv
    if '--debug' in server_args:
        server_args.remove('--debug')
    if '-d' in server_args:
        server_args.remove('-d')
    if '-f' not in server_args and '--fragile' not in server_args:
        server_args.append('--fragile')
    if nolaunch:
        if '-n' not in server_args and '--nolaunch' not in server_args:
            server_args.append('--nolaunch')
    return server_args


def main():
    parser = ArgumentParser(description='DVDev: Distributed Versioned Development')
    parser.add_argument('repositories', metavar='repository', type=str, nargs='*', default=[
     os.getcwd()], help='List of repositories to serve. If left blank, DVDev will search the current and subdirectories for existing repositories.')
    parser.add_argument('-d', '--debug', action='store_true', default=False, help="Start dvdev in debugging mode.  This causes dvdev to monitor it's own source files and reload if they have changed.  Normally, only DVDev developers will ever have need of this functionality.")
    parser.add_argument('-f', '--fragile', action='store_true', default=False, help="INTERNAL USE ONLY.  When specified, start a thread that watches DVDev's source files.  If any change, then quit this process.")
    parser.add_argument('-c', '--create', action='store_true', default=False, help='For any directories passed in on the command line (or the current directory, if none), initialize them as a repository if they do not already contain one.')
    parser.add_argument('-n', '--nolaunch', action='store_true', default=False, help="Don't launch a web browser after starting the http server.")
    parser.add_argument('-p', '--port', type=int, default=4000, help='The port to serve on (by default: 4000).  If this port is in use, dvdev will try to randomly select an open port.')
    parser.add_argument('-i', '--ip', default='0.0.0.0', help='The IP address to listen on. Defaults to 0.0.0.0, which means all IPv4 addresses')
    args = parser.parse_args()
    if args.debug:
        nolaunch = args.nolaunch
        while True:
            child = None
            try:
                try:
                    print 'Launching server process'
                    (exit_code, child) = launch_and_watch_child(_server_args(args, nolaunch))
                    if not child:
                        break
                    nolaunch = True
                except (SystemExit, KeyboardInterrupt):
                    return

            finally:
                if child and hasattr(os, 'kill'):
                    try:
                        os.kill(child, signal.SIGTERM)
                    except (OSError, IOError):
                        pass

            if exit_code != 3:
                return exit_code

    if args.fragile:
        from paste import reloader
        reloader.install()
    for (index, repository) in enumerate(args.repositories):
        if os.path.exists(repository):
            continue
        myui = ui.ui()
        myui.pushbuffer()
        from urllib2 import URLError
        try:
            commands.clone(myui, repository)
        except (RepoError, URLError):
            if args.create:
                try:
                    os.makedirs(repository)
                    try:
                        commands.init(myui, repository)
                        continue
                    except:
                        os.unlink(repository)

                except IOError:
                    pass

            print 'Bad repository: %s' % repository
            import sys
            sys.exit(1)

        destination = myui.popbuffer().split('\n')[0]
        destination = destination.split('destination directory: ')[1]
        if not os.path.exists(destination):
            print 'Successfully cloned repository %s but unable to read local copy at %s' % (
             repository, destination)
            import sys
            sys.exit(1)
        print 'Cloned repository %s in local directory %s' % (repository, destination)
        args.repositories[index] = destination

    if args.create:
        all_repos = []
        for repo in args.repositories:
            found_repos = flatten(build_repo_tree(repo))
            if not found_repos:
                myui = ui.ui()
                commands.init(myui, repo)
            else:
                all_repos += found_repos

    else:
        all_repos = filter(None, flatten([ build_repo_tree(repo) for repo in args.repositories ]))
    print 'All repositories: %r' % all_repos
    config = {'use': 'egg:DVDev', 
       'full_stack': 'true', 
       'static_files': 'true', 
       'reporoot': os.getcwd(), 
       'cache_dir': os.path.join(os.getcwd(), 'data'), 
       'beaker.session.key': 'dvdev', 
       'beaker.session.secret': 'somesecret', 
       'repo': (' ').join(all_repos), 
       'project_home': 'issues', 
       'who.log_level': 'debug', 
       'who.log_file': 'stdout', 
       'workspace': os.path.join(os.getcwd(), 'workspace')}
    from dvdev.config.middleware import make_app
    app = make_app({'debug': (args.debug or args.fragile) and 'true' or 'false'}, **config)
    import webbrowser

    def webhelper(url):
        """        Curry the webbrowser.open method so that we can cancel it with a
        threaded timer."""

        def _launch_closure():
            webbrowser.open(url)

        return _launch_closure

    if not args.nolaunch:
        from threading import Timer
        safelaunch = Timer(0.7, webhelper('http://%s:%d/' % (args.ip, args.port)))
        safelaunch.start()
    import socket
    from paste.httpserver import serve
    try:
        serve(app, host=args.ip, port=args.port)
    except socket.error, e:
        safelaunch.cancel()
        print 'Unable to serve on port %d : Error message was: %s' % (args.port, e[1])

    return


if __name__ == '__main__':
    main()