# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sesame2/allegro.py
# Compiled at: 2010-01-19 08:40:15
__author__ = 'Cosmin Basca'
import sesame2
from urllib import urlencode
import httplib, os, os.path, shutil

class AllegroException(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(sel):
        return 'Allegro Exception : %s' % self.msg


class Allegro(sesame2.Sesame2):

    def __init__(self, host, port=80, root_path='/sesame', directory='', strict=False):
        sesame2.Sesame2.__init__(self, host, port, root_path, strict)
        sesame2.Sesame2.url['load'] = '/repositories/%(id)s/load'
        sesame2.Sesame2.url['index'] = '/repositories/%(id)s/index'
        sesame2.Sesame2.url['map'] = '/repositories/%(id)s/map'
        self.directory = directory.strip()
        if self.directory:
            if not os.path.exists(self.directory):
                try:
                    os.makedirs(self.directory)
                except:
                    raise AllegroException('could not create repository folder [%s]' % self.directory)

    def open_repository(self, id, name=None):
        return self.create_repository(id, '', name=name, if_exists='open')

    def create_repository(self, id, title, name=None, if_exists='open', readable=True, writable=True):
        params = {'id': id, 'readable': 'true' if readable else 'false', 
           'writable': 'true' if writable else 'false', 
           'if-exists': if_exists, 
           'title': title}
        if self.directory:
            params['directory'] = self.directory
        if name:
            params['name'] = name
        try:
            self.sesame2_request('POST', 'repositories', params=params)
        except sesame2.Sesame2Exception:
            return False

        return True

    def remove_repository(self, name):
        """
        warning: works only locally!, do not use otherwise
        """
        if self.directory:
            try:
                shutil.rmtree(os.path.join(self.directory, name))
            except:
                return False
            else:
                return True
        return False

    def load_statements(self, id, location, update=True, format='rdf', context=None, baseURI=None, externalFormat=None, saveStrings=False):
        method = 'PUT'
        if update:
            method = 'POST'
        params = {format: location}
        if context:
            params['context'] = context
        if format == 'rdf':
            if baseURI:
                params['baseURI'] = baseURI
        elif format == 'ntriple':
            params['saveStrings'] = saveStrings
            if externalFormat:
                params['externalFormat'] = externalFormat
        try:
            self.sesame2_request(method, 'load', {'id': str(id)}, params=params)
        except sesame2.Sesame2Exception:
            return False

        return True

    def index_info(self, id):
        return self.sesame2_request('GET', 'index', {'id': id})

    def mappings(self, id):
        return self.sesame2_request('GET', 'map', {'id': id})


if __name__ == '__main__':
    allegro = Allegro('localhost', 5678, '/sesame', 'd:\\repositories')
    print 'Protocol : ', allegro.protocol()
    print 'Open :', allegro.open_repository('corona')
    print 'Repositories : ', allegro.repositories()