# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/ENV2/lib/python2.7/site-packages/cloudmesh/rest/service.py
# Compiled at: 2017-04-12 13:00:41
__doc__ = '\nThe EVE REST service management \n'
import os, sys
from pprint import pprint
from cloudmesh.common.console import Console
from eve import Eve

class RestService(object):
    """
    The REST service methods
    """

    def __init__(self, settings=None):
        self.name = 'eve'
        self.settings = settings
        self.app = None
        return

    def info(self):
        return self.parameters

    def run(self):
        """
        start the REST service
        :return: 
        """
        Console.ok('loading eve_settings ...')
        sys.path.append('~/.cloudmesh/eve')
        from settings import eve_settings
        Console.ok('loaded.')
        pprint(eve_settings)
        app = Eve(settings=eve_settings)
        app.run()

    def start(self):
        os.system('cms admin rest run &')

    def stop(self):
        """
        stop the rest service
        :return: 
        """
        print 'NOT YET IMPLEMENTED'

    def status(self):
        """
        return the status of the rest service
        :return: 
        """
        print 'NOT YET IMPLEMENTED'

    def reset(self, settings=None):
        """
        reset the restservice by deleting the database, initialising the settings.py and restart the service
        :param settings: 
        :return: 
        """
        print 'NOT YET IMPLEMENTED'


def main():
    """
    TODO: a simple example, which should actully be in a nosetest
    :return: 
    """
    app = Eve(settings=eve_settings)
    app.run()


if __name__ == '__main__':
    main()