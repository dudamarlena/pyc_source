# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/actions.py
# Compiled at: 2016-02-25 16:45:11
from github3 import login
from .book import Book

def get_id(repo):
    book = Book(None, repo_name=repo)
    repo = book.github_repo.github.repository('GITenberg', repo)
    print repo.id
    return repo.id


def delete(repo_name):
    book = Book(None, repo_name=repo_name)
    repo = book.github_repo.github.repository('GITenberg', repo_name)
    if repo:
        if repo.delete():
            print ('{} deleted').format(repo_name)
        else:
            print ("couldn't delete {}").format(repo_name)
    else:
        print ("{} didn't exist").format(repo_name)
    return