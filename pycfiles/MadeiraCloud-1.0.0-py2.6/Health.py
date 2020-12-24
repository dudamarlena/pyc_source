# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/madeiracloud/Health.py
# Compiled at: 2011-12-16 02:01:38
import logging

def _amazon(mode, ns):
    pass


def _redhat(mode, ns):
    pass


def _centos(mode, ns):
    pass


def _debian(mode, ns):
    pass


def _ubuntu(mode, ns):
    pass


def _suse(mode, ns):
    pass


Distro = {'amazon': _amazon, 
   'redhat': _redhat, 
   'centOS': _centos, 
   'debian': _debian, 
   'ubuntu': _ubuntu, 
   'suse': _suse}

def run(endpoint, key, distro):
    status = {}
    try:
        status = Distro[distro]()
        server = Server(endpoint)
        if not server.report(key, status):
            raise Exception
    except:
        logging.error('Failed to report system health')