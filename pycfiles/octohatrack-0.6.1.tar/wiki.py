# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: octohatrack/wiki.py
# Compiled at: 2016-05-01 22:01:57
from git import Repo
import os, shutil, sys, requests
from .helpers import progress, progress_advance, get_user_data
tmp_folder = 'tmprepo'

def get_wiki_contributors(repo_name):
    if not shutil.which('git'):
        print "Cannot find local 'git' installation. Skipping wiki contributions"
        return []
    else:
        wiki_url = 'https://github.com/%s.wiki' % repo_name
        resp = requests.get('https://github.com/%s/wiki' % repo_name)
        if 'Clone this wiki locally' not in resp.text:
            return []
        progress('Collecting wiki contributors')
        progress_advance()
        try:
            if os.path.isdir(tmp_folder):
                shutil.rmtree(tmp_folder)
            repo = Repo.clone_from(wiki_url, tmp_folder)
        except ValueError as e:
            print '\nError attempting clone wiki: %s' % str(e)
            return []

        progress_advance()
        wiki_contributors = []
        for i in list(repo.iter_commits('master')):
            wiki_contributors.append(i.author)

        response = list(set(wiki_contributors))
        users = []
        for entry in response:
            user = get_user_data({'login': str(entry), 'avatar_url': ''})
            if user is not None:
                users.append(user)

        return users