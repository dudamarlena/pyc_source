# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/big/ENV2/lib/python2.7/site-packages/cloudmesh_vagrant/image/image.py
# Compiled at: 2016-05-24 07:16:41
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.shell.console import Console
import os

class image(object):

    @classmethod
    def list(cls):

        def convert(line):
            line = line.replace('(', '')
            line = line.replace(')', '')
            line = line.replace(',', '')
            entry = line.split(' ')
            data = dotdict()
            data.name = entry[0]
            data.provider = entry[1]
            data.date = entry[2]
            return data

        result = Shell.execute('vagrant', ['box', 'list'])
        lines = []
        for line in result.split('\n'):
            lines.append(convert(line))

        return lines

    @classmethod
    def add(cls, name):
        result = Shell.execute('vagrant', ['box', 'add', name])
        return result

    @classmethod
    def find(cls, name):
        Console.error('not yet implemented')
        d = {'key': name}
        os.system('open ' + ('https://atlas.hashicorp.com/boxes/search?utf8=\\&sort=\\&provider=\\&q={key}').format(**d))