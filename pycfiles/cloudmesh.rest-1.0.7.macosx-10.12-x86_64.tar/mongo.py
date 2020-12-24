# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/ENV2/lib/python2.7/site-packages/cloudmesh/rest/mongo.py
# Compiled at: 2017-04-12 13:00:41
"""
The interface to Mongo
"""
from __future__ import print_function
import os, shutil
from pprint import pprint
import psutil
from cloudmesh.common.Shell import Shell
from cloudmesh.common.console import Console

class Mongo(object):
    """
    Manage mongod service.
    """

    def info(self):
        """
        returs the internal parameters
        :return: 
        """
        self.parameters['pid'] = self.pid()
        self.parameters['status'] = self.status()
        return self.parameters

    def __init__(self, port=27017):
        """
        sets up a mongo d service
        :param port: the port number. default set to 5000
        """
        self.name = 'mongo'
        self.parameters = {'name': 'mongo', 
           'port': port, 
           'dbpath': '~/.cloudmesh/data/db', 
           'bind_ip': '127.0.0.1', 
           'logpath': '~/.cloudmesh/data/db/mongo.log', 
           'pid': None, 
           'status': None}
        r = Shell.mkdir(self.parameters['dbpath'])
        return

    def clean(self):
        """
        Removes the database and the log files
        :return:
        """
        shutil.rmtree(self.parameters['dbpath'])
        shutil.rmtree(self.parameters['logpath'])
        r = Shell.mkdir(self.parameters['dbpath'])
        Console.msg(r)

    def kill(self):
        """
        killall mongod
        :return:
        """
        os.system('killall mongod')
        self.clean()

    def start(self):
        """starts the mongo service."""
        command = ('ulimit -n 1024; mongod --port {port} -dbpath {dbpath} -bind_ip {bind_ip} --fork --logpath {logpath}').format(**self.parameters)
        r = Shell.mkdir(self.parameters['dbpath'])
        Console.msg(r)
        Console.msg(command)
        os.system(command)
        Console.ok('started')
        self.status()

    def stop(self):
        """stops the mongo service."""
        process_id = self.pid()
        if process_id is not None:
            p = psutil.Process(int(process_id))
            p.terminate()
        Console.ok('stopped')
        self.status()
        return

    def pid(self):
        """
        return the PID of the mongo provcesses
        :return: 
        """
        process_id = None
        output = Shell.ps('-ax')
        for line in output.split('\n'):
            if 'mongod' in line and '--port' in line:
                process_id = line.split(' ')[0]
                return process_id

        return process_id

    def status(self, format=None):
        """returns the status of the service. if no parameter. if format
        is specified its returned in that format. txt, json, XML,
        allowed
        """
        process_id = self.pid()
        if process_id is not None:
            return 'running'
        else:
            return 'stopped'
            return

    def reset(self):
        """stops the service and deletes the database, restarts the service."""
        pass

    def delete(self):
        """deletes all data in the database."""
        try:
            Console.error('NOT YET IMPLEMENTED')
        except Exception as e:
            Console.error('problem deleting' + str(e))

    def log(self, path):
        """
        sets the log file to the given path
        :param path: the path to the logfile
        """
        self.parameters['logpath'] = path


if __name__ == '__main__':
    m = Mongo()
    m.start()