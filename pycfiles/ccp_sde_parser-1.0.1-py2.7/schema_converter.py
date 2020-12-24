# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/ccp_sde_parser/schema_converter.py
# Compiled at: 2012-11-04 23:12:00
"""Parses a MS SQL Server script that contains CREATE TABLE statements, and converts it to JSON."""
import json, os
from progressbar import ProgressBar, Bar, ETA, Percentage
import re, StringIO, sys
LINE_REGEX = re.compile('^\\s+(\\w+)\\s+.*(text|char|int|float|real|money|datetime|bit).*,')
SCHEMA_TYPE = dict(int='integer', float='float', real='float', bit='boolean')

class Lexer(object):
    """Provides a way to iterate over input with possible backup and errors."""

    def __init__(self, inp):
        self._inp = inp[:]
        self._idx = 0
        self.output = dict()
        self.pbar = ProgressBar(widgets=['Converting... ', Bar(), ' ', Percentage(), ' ', ETA()], maxval=len(inp))

    def __iter__(self):
        """The core of the lexer. Explicitly written to allow the current index to change, for backup purposes."""
        while True:
            l = self.get_one_line()
            if not l:
                return
            self.pbar.update(self._idx)
            yield l

    def backup(self, i):
        """Moves the current index into the input backward by `i` lines."""
        self._idx = self._idx - i
        if self._idx < -1:
            self._idx = -1

    def error(self, msg):
        """Renders an error to stderr, adding information about the current line."""
        sys.stderr.write('Error!!\n')
        sys.stderr.write(msg + '\n')
        sys.stderr.write('At line #%s\n' % self._idx)
        self.output = []

    def get_one_line(self):
        """Steps the lexer forward one line, returning it."""
        self._idx += 1
        if self._idx > len(self._inp):
            return None
        else:
            return '%s\n' % self._inp[(self._idx - 1)]

    def run(self):
        """Actually starts the whole lexer going."""
        self.pbar.start()
        state = startState
        while state:
            state = state(self)

        self.pbar.finish()


def constraintState(lexer):
    """Parses the bodies of CONSTRAINT clauses, so we know which columns are primary."""
    lexer.get_one_line()
    for line in lexer:
        if line.startswith(')'):
            lexer.backup(1)
            return startState
        field = re.search('\\[(\\w+)\\]', line).group(1)
        lexer.output[lexer.curr_table][field] = (lexer.output[lexer.curr_table][field][0], True)

    lexer.error('Reached end of file before end of CONSTRAINT clause!\nTable: %s' % lexer.curr_table)
    return


def createTableState(lexer):
    """Parses CREATE TABLE clauses"""
    line = lexer.get_one_line()
    if not line or not line.startswith('CREATE TABLE'):
        lexer.error('Malformed CREATE TABLE stanza.')
        return None
    else:
        table_name = line[20:-3]
        lexer.curr_table = table_name
        lexer.output[table_name] = dict()
        for line in lexer:
            if 'CONSTRAINT' in line:
                return constraintState
            line = line.replace('[', '').replace(']', '')
            m = LINE_REGEX.match(line)
            if not m:
                lexer.error('Could not match the LINE_REGEX to this value!\nSaw line: %s' % line)
                return None
            lexer.output[table_name][m.group(1)] = (SCHEMA_TYPE.get(m.group(2), 'string'), False)

        return startState


def startState(lexer):
    """Eats input until it hits CREATE TABLE, then hands off to createTableState"""
    for line in lexer:
        if line.startswith('CREATE TABLE'):
            lexer.backup(1)
            return createTableState

    return


def main():
    if len(sys.argv) != 3:
        sys.stderr.write('Incorrect number of arguments.\n')
        sys.stderr.write('USAGE: %s SQL_SCRIPT OUTPUT_FILE\n' % sys.argv[0])
        sys.exit(1)
    sql_script = sys.argv[1]
    output_file = sys.argv[2]
    if not os.path.isfile(sql_script):
        sys.stderr.write('Unable to access file %s\n' % sql_script)
        sys.exit(1)
    inp = None
    with open(sql_script) as (sql_file):
        inp = sql_file.read().splitlines()
    lexer = Lexer(inp)
    lexer.run()
    with open(output_file, 'w') as (out_file):
        json.dump(lexer.output, out_file, sort_keys=True, indent=2)
    return


if __name__ == '__main__':
    main()