# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/takada-at/python2/lib/python2.7/site-packages/tests/conftest.py
# Compiled at: 2015-12-15 06:37:55
from __future__ import absolute_import, division, print_function
import boto, os
from pathlib import Path
import moto, shutil, tempfile
from sg.client import Config

def pytest_funcarg__tempdir(request):

    def final():
        shutil.rmtree(tempdir)

    tempdir = tempfile.mkdtemp()
    request.addfinalizer(final)
    os.chdir(tempdir)
    return Path(tempdir)


def pytest_funcarg__config(request):
    tempdir = pytest_funcarg__tempdir(request)
    with (tempdir / 'aws_key').open('w') as (fio):
        fio.write('dummy:dummy')
    config = Config('sge.cfg')
    config.region = None
    return config


def pytest_funcarg__mock_groups(request):

    def end():
        mock.stop()

    mock = moto.mock_ec2()
    mock.start()
    con = boto.connect_ec2()
    group = con.create_security_group('mock-group', 'hoge')
    group2 = con.create_security_group('mock-group2', 'description')
    group.authorize(ip_protocol='tcp', from_port=22, to_port=22, cidr_ip='192.168.1.0/32')
    group.authorize(ip_protocol='tcp', from_port=22, to_port=22, src_group=group2)
    request.addfinalizer(end)
    return [group, group2]


def pytest_funcarg__files(request):
    from sg.client import AwsClient
    from sg.service import SgService
    config = pytest_funcarg__config(request)
    pytest_funcarg__mock_groups(request)
    tempdir = config.base_path
    client = AwsClient(config)
    path_list = SgService.save_groups(config, client, tempdir / 'security_groups', noconfirm=True)
    return path_list