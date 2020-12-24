# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/madeiracloud/Task.py
# Compiled at: 2011-12-16 02:01:38
import logging
from xml.dom import minidom
import script
Script = {'/etc/hosts': script._etc_hosts}

def run(endpoint, key, distro):
    res = {}
    try:
        server = Server(endpoint)
        (err, data) = server.get(key)
        if err:
            raise Exception('Failed to get new task')
        tasks = data[1]
        if not taks:
            logging.info('No pending task')
            raise Exception
        for t in tasks:
            if not Script.has_key(t['code'][0]):
                logging.error('Invalid script code: %s' % t['code'][0])
                raise Exception
            res[t['id'][0]] = Script[t['code'][0]].do(t['params'], distro)
            if res[t['id'][0]] is not None:
                logging.info('Successfully executed script %s with parameters %s' % (task['code'][0], task['params'][0]))

    except:
        logging.error('Error during executing pending task')

    return