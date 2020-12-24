# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/git_additions/logs/logs.py
# Compiled at: 2018-12-30 14:19:13
import os, pygit2
from git_additions.__helpers import duration, commit_date, find_toplevel
from git_additions.exporter.csv_exporter import CSVExporter
from git_additions.logs.print_log import PrintLog

class Logs(object):

    def __init__(self, options):
        self.lines = []
        self.__options = options
        if options.output is not None:
            self.exporter = CSVExporter()
        return

    def report(self):
        last_commit = None
        first_commit = None
        repo = pygit2.Repository('%s/.git' % find_toplevel(os.getcwd()))
        for commit in repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL | pygit2.GIT_SORT_REVERSE):
            if self.__options.author is not None and commit.author.name != self.__options.author:
                continue
            if self.__options.email is not None and commit.author.email != self.__options.email:
                continue
            line = [
             commit_date(commit), commit.author.name, commit.author.email]
            if last_commit is not None:
                dur = duration(last_commit, commit)
                line.append('%d %02d:%02d:%02d' % dur)
            else:
                line.append('0 00:00:00')
            line.append(commit.message.strip())
            if first_commit is None:
                first_commit = commit
            last_commit = commit
            self.lines.append(line)

        if self.__options.output is not None:
            headers = [
             'Time', 'Author', 'Email', 'Duration', 'Message']
            self.exporter.set_lines([headers] + self.lines)
            self.exporter.write_content(self.__options.output)
        else:
            PrintLog(self.lines).run()
        return