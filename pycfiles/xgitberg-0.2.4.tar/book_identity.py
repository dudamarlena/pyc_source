# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/book_identity.py
# Compiled at: 2016-02-05 15:21:16


class BookRepoName(object):
    """ A representation of the identity of a Gitenberg book.
    :takes: <book_repo_name> - GITenberg repo name `Frankenstein_84`
    :provides: `class.repo_name` - local folder identifier,
                                    currently GITenberg repo name
    """

    def __init__(self, repo_name):
        self.repo_name = repo_name
        self.clone_url_ssh_template = 'git@github.com:GITenberg/{repo_name}.git'

    def get_clone_url_ssh(self):
        return self.clone_url_ssh_template.format(repo_name=self.repo_name)