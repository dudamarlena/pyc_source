# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/commentdater/src.py
# Compiled at: 2019-12-23 18:03:17
# Size of source mod 2**32: 4489 bytes
"""
Created on Tue Dec 17 15:53:52 2019

@author: lavanyasingh
"""
__version__ = '0.1.0'
import os, sys, argparse

class CommentDater:
    DIFF_FILE = 'diffs.txt'

    def __init__(self, file, output_len=50):
        self.file = file
        self.diffs = []
        self.comments = []
        self.find_lines()
        self.output_len = output_len

    def get_diffs(self):
        pid = os.fork()
        if pid == 0:
            args = [
             'git', 'diff', 'HEAD~1', '-U0', self.file]
            outfile = open(self.DIFF_FILE, 'w+')
            os.dup2(outfile.fileno(), sys.stdout.fileno())
            r = os.execvp(args[0], args)
            if r != 0:
                print('child process failed to execvp')
                os._exit(1)
        r = os.waitpid(pid, 0)

    def parse_line(self, line):
        line = line[line.find('+') + 1:]
        end = line.find(',')
        if end == -1:
            end = line.find(' @')
        return line[:end]

    def find_lines(self, diff_file=None):
        self.get_diffs()
        if not diff_file:
            diff_file = self.DIFF_FILE
        with open(diff_file, 'r') as (fd):
            lines = list(iter(fd.readline, ''))
        lines = list(filter(lambda s: s.find('@@') != -1, lines))
        for i in range(len(lines)):
            lines[i] = self.parse_line(lines[i])

        lines = list(map(lambda s: int(s), lines))
        self.diffs = lines
        return lines

    def is_comment(self, line):
        return line.find('//') != -1 and line.count('"', 0, line.find('//')) % 2 == 0

    def find_comments(self):
        with open(self.file, 'r') as (fd):
            seen = set()
            comments = []
            lineno = 1
            last_comment = None
            lines = list(iter(fd.readline, ''))
            for line in lines:
                if self.is_comment(line):
                    last_comment = lineno
                if lineno in self.diffs:
                    if last_comment:
                        if lineno != last_comment:
                            if last_comment not in seen:
                                if last_comment not in self.diffs:
                                    seen.add(last_comment)
                                    comments.append((last_comment, lines[(last_comment - 1)], lineno, line))
                lineno += 1

        self.comments = list(comments)
        return list(comments)

    def build_output(self):
        string = '\n'
        output_len = self.output_len
        for comment in self.comments:
            string += 'possible outdated comment at ' + self.file + ':' + str(comment[0]) + ':\n\t "'
            string += comment[1][0:output_len].replace('\n', '').strip()
            if len(comment[1]) > output_len:
                string += '...'
            string += '"\nfor diff at ' + self.file + ':' + str(comment[2]) + ':\n\t "'
            string += comment[3][0:output_len].replace('\n', '').strip()
            if len(comment[3]) > output_len:
                string += '...'
            string += '"\n\n'

        print(string, end='')

    def parse(self):
        self.find_comments()
        self.build_output()
        os.remove(self.DIFF_FILE)


def create_parser():
    argp = argparse.ArgumentParser(description='Check if your comments are out of date')
    argp.add_argument('-f', '--file', type=str, help='file to check', required=True)
    return argp


def main():
    argp = create_parser()
    args = argp.parse_args()
    dater = CommentDater(args.file)
    dater.parse()