# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/extraction/tests/test_usernames.py
# Compiled at: 2015-09-05 21:24:22
from __future__ import absolute_import
import pytest
from dossier.fc import StringCounter
from dossier.extraction import usernames
example_usernames_from_paths = [
 ('http://www.example.com/user/folder3/index.html?source=dummy', 'folder3', 3),
 ('http://www.example.com/user/myaccount', 'myaccount', 2),
 ('http://www.different.com/folder3', None, 4),
 ('http://www.different.com/user/myaccount', 'myaccount', 7),
 ('http://www.also.com/user', None, 23),
 ('http://www.also2.com/user/user', 'user', 1),
 ('http://frob.com/user/my_account/media/Dresses/hi.jpg', 'my_account', 1),
 ('https://www.facebook.com/my_account', 'my_account', 1),
 ('https://twitter.com/my_account', 'my_account', 1),
 ('C:\\WINNT\\Profiles\\myaccount%MyUserProfile%', 'myaccount', 3),
 ('C:\\WINNT\\Profiles\\myaccount', 'myaccount', 3),
 ('d:\\WINNT\\Profiles\\myaccount', 'myaccount', 3),
 ('X:\\Documents and Settings\\myaccount', 'myaccount', 8),
 ('C:\\Users\\myaccount', 'myaccount', 3),
 ('C:\\Users\\myaccount\\dog', 'myaccount', 3),
 ('C:\\Users\\whg\\Desktop\\Plug\\FastGui(LYT)\\Shell\\Release\\Shell.pdb', 'whg', 2),
 ('C:\\Documents and Settings\\whg\\\\Plug\\FastGui(LYT)\\Shell\\Release\\Shell.pdb',
 'whg', 3),
 ('C:\\Users\\whg\\Desktop\\Plug\\FastGui(LYT)\\Shell\\Release\\Shell.pdb', 'whg', 3),
 ('/home/myaccount$HOME', 'myaccount', 5),
 ('/var/users/myaccount', 'myaccount', 3),
 ('/u01/myaccount', 'myaccount', 3),
 ('/user/myaccount', 'myaccount', 3),
 ('/users/myaccount', 'myaccount', 3),
 ('/var/users/myaccount', 'myaccount', 3),
 ('/home/myaccount', 'myaccount', 3),
 ('/Users/my_account$HOME', 'my_account', 5),
 ('/Users/my_account', 'my_account', 5),
 ('/data/media/myaccount', 'myaccount', 5)]

@pytest.mark.parametrize(('url_or_path', 'username', 'count'), example_usernames_from_paths)
def test_usernames(url_or_path, username, count):
    urls = StringCounter()
    urls[url_or_path] += count
    if username is not None:
        results = usernames(urls)
        assert results == StringCounter({username: count})
    return