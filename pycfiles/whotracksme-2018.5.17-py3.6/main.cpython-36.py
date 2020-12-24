# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/whotracksme/main.py
# Compiled at: 2018-05-17 05:30:15
# Size of source mod 2**32: 1963 bytes
"""
Whotracks.me website development tool.

Usage:
    whotracksme website [serve]
    whotracksme data [list]
    whotracksme db (create|dump|check_urls)
    whotracksme -h | --help

Options:
    serve           Watch for changes and reload.
    -h, --help      Show help message.
"""
from pathlib import Path
import os, sqlite3, docopt
from whotracksme.website.builder import Builder
from whotracksme.website.serve import serve
from whotracksme.data.loader import load_tracker_db
from whotracksme.qa.todo import upgrade_to_https, create_task_files

class objectview:
    __doc__ = "Allows to access keys of a dictionary as attributes.\n\n    Example:\n        >>> view = objectview({ 'foo': True, 'bar': False })\n        >>> view.foo\n        True\n        >>> view.bar\n        False\n    "

    def __init__(self, d):
        self.__dict__ = d


def website(args):
    builder = Builder()
    builder.build()
    if args.serve:
        serve(builder)


def main():
    args = objectview(docopt.docopt(__doc__))
    if args.website:
        website(args)
    else:
        if args.data:
            pass
        elif args.db:
            if args.create:
                load_tracker_db(loc='tracker.db')
            else:
                if args.dump:
                    tracker_db_path = os.path.join(os.path.dirname(__file__), 'data', 'assets', 'trackerdb.sql')
                    conn = sqlite3.connect('tracker.db')
                    with open(tracker_db_path, 'w') as (fp):
                        for line in conn.iterdump():
                            fp.write('%s\n' % line)

            if args.check_urls:
                needqa = Path('needqa')
                if not needqa.exists():
                    needqa.mkdir()
                https_upgrade = upgrade_to_https(tracker_db='tracker.db')
                create_task_files(needqa_folder=needqa, **https_upgrade)


if __name__ == '__main__':
    main()