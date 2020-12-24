# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/models/tests/test_features.py
# Compiled at: 2015-07-08 07:34:06
"""``dossier.models.features.basic`` provides simple transforms that
construct features.

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2015 Diffeo, Inc.

"""
import json, pytest
from dossier.models.tests import nltk_data, example_fc
from dossier.fc import StringCounter, FeatureCollection
import dossier.models.features as features

def test_extract_phones():
    txt = '\nPhone: 111-222-3333\nPhone: 1112223333\nPhone: 1-111-222-3333\nPhone: 11112223333\nPhone: 222-3333\nPhone: 2223333\n'
    assert StringCounter(features.phones(txt)) == StringCounter({'1112223333': 2, 
       '11112223333': 2, 
       '2223333': 2})


def test_a_urls():
    html = '\n<a href="http://ExAmPle.com/My Page.html">\n<a href="http://example.com/My%20Page.html">\n'
    assert StringCounter(features.a_urls(html)) == StringCounter({'http://example.com/My Page.html': 2})


def test_image_urls():
    html = '\n<img src="http://ExAmPle.com/My Image.jpg">\n<img src="http://example.com/My%20Image.jpg">\n'
    assert StringCounter(features.image_urls(html)) == StringCounter({'http://example.com/My Image.jpg': 2})


def test_extract_emails():
    txt = '\nemail: abc@example.com\nemail: AbC@eXamPle.com\n'
    assert StringCounter(features.emails(txt)) == StringCounter({'abc@example.com': 2})


def test_host_names():
    urls = StringCounter()
    urls['http://www.example.com/folder1'] = 3
    urls['http://www.example.com/folder2'] = 2
    urls['http://www.different.com/folder2'] = 7
    assert features.host_names(urls) == StringCounter({'www.example.com': 5, 
       'www.different.com': 7})


def test_path_dirs():
    urls = StringCounter()
    urls['http://www.example.com/folder1/folder3/index.html?source=dummy'] = 3
    urls['http://www.example.com/folder2/folder1'] = 2
    urls['http://www.different.com/folder2'] = 7
    assert features.path_dirs(urls) == StringCounter({'folder1': 5, 
       'folder2': 9, 
       'folder3': 3, 
       'index.html': 3})


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
        results = features.usernames(urls)
        assert results == StringCounter({username: count})
    return


def test_entity_names(example_fc, nltk_data):
    """test for the `entity_names` transform
    """
    xform = features.entity_names()
    fc = xform.process(example_fc)
    assert 'PERSON' in fc, fc.keys()
    assert 'craig winton' in fc['PERSON']