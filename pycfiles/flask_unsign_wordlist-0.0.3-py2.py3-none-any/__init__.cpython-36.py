# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Paradoxis/Documents/Projects/flask-unsign-wordlist/flask_unsign_wordlist/__init__.py
# Compiled at: 2019-01-26 07:13:03
# Size of source mod 2**32: 894 bytes
__version__ = '0.0.3'
__url__ = 'https://github.com/Paradoxis/Flask-Unsign-Wordlist'
__author__ = 'Luke Paris (Paradoxis)'
import os, sys
from flask_unsign_wordlist.exceptions import NoSuchWordlist

def get(name: str='all') -> str:
    """
    Get the path to a flask-unsign wordlist
    :param name: Wordlist name ('.txt' is implied)
    :return: Absolute path to a wordlist
    """
    cwd = os.path.dirname(__file__)
    path = os.path.join(cwd, 'wordlists', name + '.txt')
    if not os.path.isfile(path):
        raise NoSuchWordlist(f"No known wordlist found with name: {name!r}")
    return path


def main():
    """CLI entry point"""
    try:
        path = get(sys.argv[1] if len(sys.argv) != 1 else 'all')
        sys.stdout.write(path)
    except NoSuchWordlist as e:
        print((str(e)), file=(sys.stderr))
        return 1


if __name__ == '__main__':
    exit(main() or 0)