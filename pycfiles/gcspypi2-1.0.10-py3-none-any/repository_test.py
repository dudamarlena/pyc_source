# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/manuel/gcspypi/test/repository_test.py
# Compiled at: 2018-11-22 07:00:57
from __future__ import unicode_literals
from .mocks.mock_repository import MockRepository as Repository
import six, time
from io import BytesIO

def test_content():
    repo = Repository()
    repo.upload_content(b'object/x', b'hello world')
    assert repo.exists(b'object/x')
    assert repo.download_content(b'object/x') == b'hello world'


def test_file():
    repo = Repository()
    io = BytesIO((b'hello world').encode(b'utf-8'))
    repo.upload_file(b'object/x', io)
    assert repo.exists(b'object/x')
    assert repo.download_content(b'object/x').decode(b'utf-8') == b'hello world'


def test_list():
    repo = Repository()
    repo.upload_content(b'object/x/y', b'hello world')
    repo.upload_content(b'object/x/z', b'hello world')
    assert len(repo.list(b'object/x')) == 2
    assert len(repo.list(b'object/x/y')) == 1
    assert len(repo.list(b'object/x/z')) == 1
    assert len(repo.list(b'object/x/w')) == 0


def test_metadata():
    repo = Repository()
    repo.upload_content(b'object/x', b'hello world')
    time.sleep(0.01)
    repo.upload_content(b'object/y', b'hello world')
    xm = repo.metadata(b'object/x')
    ym = repo.metadata(b'object/y')
    assert xm.md5 == ym.md5
    assert xm.time_created < ym.time_created