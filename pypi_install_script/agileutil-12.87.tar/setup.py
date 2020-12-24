#!/usr/bin/env python

'''
pub.sh

#!/bin/sh
rm -rf ./agileutil.egg-info
rm -rf ./build
rm -rf ./dist
rm -rf ./*.tar.gz
python setup.py sdist
twine upload -u [username] -p [password] dist/*
python setup.py install
'''

DEFINE_VERSION = '12.87'

from setuptools import setup
import platform
try:
    import commands as commands
except:
    import subprocess as commands

system = platform.system()

#install begin.
"""
if system == 'Linux':
    cmd = 'yum install -y python-devel libffi libffi-devel openssl openssl-devel'
    print(cmd)
    commands.getstatusoutput(cmd)
    cmd = 'sudo apt-get install -y python-dev libldap2-dev libsasl2-dev libssl-dev build-essential autoconf libtool pkg-config python-opengl python-imaging python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python-dev libssl-dev libffi-dev libsasl2-dev python-dev libldap2-dev libssl-dev libmysqlclient-dev'
    print(cmd)
    commands.getstatusoutput(cmd)
    cmd = 'sudo apt-get install libdb-dev python-dev python3-dev libpython3-dev libpython-dev'
    print(cmd)
    commands.getstatusoutput(cmd)
if system == 'Darwin':
    pass
"""
#install end.

webpy = 'web.py'
if platform.python_version()[0:1] == '3': webpy = 'web.py==0.40.dev1'

setup(
    name='agileutil',
    version=DEFINE_VERSION,
    description='python lib',
    author='lyc',
    license='MIT',
    platforms = "any",
    install_requires=[
        'pexpect',
        'demjson',
        'requests',
        'python-decouple',
        'PyMySQL',
        webpy,
        'DBUtils',
        'paramiko'
    ],
    classifiers=[
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='agileutil',
    packages=['agileutil'],
    include_package_data=True
)