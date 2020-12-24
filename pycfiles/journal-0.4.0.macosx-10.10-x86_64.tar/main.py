# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mbehrens/.pyenv/versions/2.7.8/lib/python2.7/site-packages/journal/main.py
# Compiled at: 2015-09-01 16:29:44
from __future__ import with_statement
import sys
from os import path, makedirs, environ
import re, argparse, string, datetime, ConfigParser, subprocess, tempfile
from journal import __version__, parse
DEFAULT_JOURNAL = '~/.journal'
DEFAULT_JOURNAL_RC = '~/.journalrc'

def parse_args():
    description = 'A CLI tool to help with keeping a work/personal journal'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--version', action='version', version=__version__)
    config_group = parser.add_argument_group('optional config arguments')
    config_group.add_argument('-c', '--config', action='store', dest='config_file', nargs='?', help='load config from [CONFIG_FILE] instead of ~/.journalrc')
    config_group.add_argument('-j', '--journal', action='store', dest='journal', nargs='?', help='add entry to [JOURNAL]')
    config_group.add_argument('-l', '--location', action='store', dest='location', nargs='?', help='store journal in [LOCATION] instead of ~/.journal')
    parser.set_defaults(config_file=DEFAULT_JOURNAL_RC, location=DEFAULT_JOURNAL)
    date_group = parser.add_argument_group('optional viewing arguments')
    date_group.add_argument('-s', '--since', action='store', metavar='DATE', dest='since', nargs='?', help='find all journal entries since a date')
    date_group.add_argument('-v', '--view', action='store', metavar='DATE', dest='view', nargs='?', help='view all journal entries on a specific date')
    main_group = parser.add_argument_group('main argument')
    main_group.add_argument('entry', nargs='*', help='text to make an entry in your journal')
    return (
     parser, parser.parse_args())


def parse_config(args):
    """
    Try to load config, to load other journal locations
    Otherwise, return default location

    Returns journal location
    """
    config_path = path.expanduser(args.config_file)
    if not path.exists(config_path):
        if args.config_file != DEFAULT_JOURNAL_RC:
            print "journal: error: config file '" + args.config_file + "' not found"
            sys.exit()
        else:
            return DEFAULT_JOURNAL
    config = ConfigParser.SafeConfigParser({'journal': {'default': '__journal'}, '__journal': {'location': DEFAULT_JOURNAL}})
    config.read(config_path)
    journal_location = config.get(config.get('journal', 'default'), 'location')
    if args.journal:
        journal_location = config.get(args.journal, 'location')
    return journal_location


def check_journal_dest(location):
    journal_dir = path.expanduser(location)
    if not path.exists(journal_dir):
        try:
            makedirs(journal_dir)
        except:
            print 'journal: error: creating journal storage directory failed'
            sys.exit()


def record_entries(journal_location, entries):
    """
    args
    entry - list of entries to record
    """
    check_journal_dest(journal_location)
    current_date = datetime.datetime.today()
    date_header = current_date.strftime('%a %I:%M:%S %Y-%m-%d') + '\n'
    with open(build_journal_path(journal_location, current_date), 'a') as (date_file):
        entry_output = date_header
        entry_output += '-' + (' ').join(entries) + '\n'
        entry_output += '\n'
        date_file.write(entry_output)


def build_journal_path(journal_location, date):
    date_filename = path.expanduser(('').join([
     journal_location, '/', date.strftime('%Y.%m.%d'), '.txt']))
    return date_filename


def get_entry(journal_location, date):
    """
    args
    date - date object
    returns entry text or None if entry doesn't exist
    """
    if not isinstance(date, datetime.date):
        return
    else:
        try:
            with open(build_journal_path(journal_location, date), 'r') as (entry_file):
                return entry_file.read()
        except IOError:
            return

        return


def daterange(start_date, end_date):
    for n in xrange((end_date - start_date).days + 1):
        yield start_date + datetime.timedelta(n)


def get_entries_since(journal_location, date):
    today = datetime.date.today()
    for single_date in daterange(date, today):
        entry = get_entry(journal_location, single_date)
        if entry:
            print entry


def get_entries_from_editor():
    editor = environ.get('EDITOR')
    if not editor:
        return []
    with tempfile.NamedTemporaryFile(suffix='txt') as (fp):
        editor = map(lambda s: s.replace('\\ ', ' '), re.split('(?<!\\\\) ', editor) + [fp.name])
        subprocess.call(editor)
        with open(fp.name, 'rb') as (temp_file):
            entries = [ x.strip() for x in temp_file.readlines() if x.strip() ]
    return entries


def main():
    parser, args = parse_args()
    journal_location = parse_config(args)
    date_parse = parse.Parse()
    if args.location:
        journal_location = args.location
    if args.journal:
        journal_location += '/' + args.journal
    check_journal_dest(journal_location)
    if args.view:
        date = date_parse.day(args.view)
        if not date:
            print 'journal: error: unknown date format'
            sys.exit()
        entry = get_entry(journal_location, date)
        if entry:
            print entry
        else:
            print 'journal: error: entry not found on date %s' % date
            sys.exit()
    elif args.since:
        date = date_parse.day(args.since)
        if not date:
            print 'journal: error: unknown date format'
            sys.exit()
        get_entries_since(journal_location, date)
    else:
        if len(args.entry) == 0:
            entries = get_entries_from_editor()
            if entries:
                record_entries(journal_location, entries)
            else:
                print 'journal: error: missing entry'
            sys.exit()
        entries = filter(string.strip, args.entry)
        if entries:
            record_entries(journal_location, entries)
        else:
            print 'journal: error: missing entry'
            sys.exit()


if __name__ == '__main__':
    main()