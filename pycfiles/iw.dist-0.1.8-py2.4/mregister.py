# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/dist/mregister.py
# Compiled at: 2008-03-20 05:18:16
"""distutils.command.register

Implements the Distutils 'register' command (register with the repository).
"""
__revision__ = '$Id: register.py 38752 2005-03-31 13:57:38Z doerwalter $'
import sys, os, string, urllib2, getpass, urlparse, StringIO
from iw.dist.core import PyPIRCCommand
from distutils.errors import *
from distutils.fancy_getopt import FancyGetopt
from distutils import log

class mregister(PyPIRCCommand):
    __module__ = __name__
    description = 'register the distribution with the Python package index'
    user_options = [('repository=', 'r', 'url of repository [default: %s]' % PyPIRCCommand.DEFAULT_REPOSITORY), ('list-classifiers', None, 'list the valid Trove classifiers'), ('show-response', None, 'display full response text from server')]
    boolean_options = [
     'verify', 'show-response', 'list-classifiers']

    def initialize_options(self):
        PyPIRCCommand.initialize_options(self)
        self.show_response = 0
        self.list_classifiers = 0

    def run(self):
        self.finalize_options()
        self.check_metadata()
        if self.dry_run:
            self.verify_metadata()
        elif self.list_classifiers:
            self.classifiers()
        else:
            self.send_metadata()

    def check_metadata(self):
        """Ensure that all required elements of meta-data (name, version,
           URL, (author and author_email) or (maintainer and
           maintainer_email)) are supplied by the Distribution object; warn if
           any are missing.
        """
        metadata = self.distribution.metadata
        missing = []
        for attr in ('name', 'version', 'url'):
            if not (hasattr(metadata, attr) and getattr(metadata, attr)):
                missing.append(attr)

        if missing:
            self.warn('missing required meta-data: ' + string.join(missing, ', '))
        if metadata.author:
            if not metadata.author_email:
                self.warn("missing meta-data: if 'author' supplied, " + "'author_email' must be supplied too")
        elif metadata.maintainer:
            if not metadata.maintainer_email:
                self.warn("missing meta-data: if 'maintainer' supplied, " + "'maintainer_email' must be supplied too")
        else:
            self.warn('missing meta-data: either (author and author_email) ' + 'or (maintainer and maintainer_email) ' + 'must be supplied')

    def classifiers(self):
        """ Fetch the list of classifiers from the server.
        """
        config = self._read_pypirc()
        if config != {}:
            self.repository = config['repository']
        response = urllib2.urlopen(self.repository + '?:action=list_classifiers')
        print response.read()

    def verify_metadata(self):
        """ Send the metadata to the package index server to be checked.
        """
        (code, result) = self.post_to_server(self.build_post_data('verify'))
        print 'Server response (%s): %s' % (code, result)

    def send_metadata(self):
        """ Send the metadata to the package index server.

            Well, do the following:
            1. figure who the user is, and then
            2. send the data as a Basic auth'ed POST.
            XXX
            1. use existing login,
             2. register as a new user, or
             3. set the password to a random string and email the user.

        """
        choice = 'x'
        username = password = ''
        config = self._read_pypirc()
        if config != {}:
            username = config['username']
            password = config['password']
            self.repository = config['repository']
            self.realm = config['realm']
            choice = '1'
        else:
            if self.repository not in ('pypi', self.DEFAULT_REPOSITORY):
                raise ValueError('%s not found in .pypirc' % self.repository)
            if self.repository == 'pypi':
                self.repository = self.DEFAULT_REPOSITORY
        choices = ('1 2 3 4').split()
        while choice not in choices:
            print 'We need to know who you are, so please choose either:\n 1. use your existing login,\n 2. register as a new user,\n 3. have the server generate a new password for you (and email it to you), or\n 4. quit\nYour selection [default 1]: ',
            choice = raw_input()
            if not choice:
                choice = '1'
            elif choice not in choices:
                print 'Please choose one of the four options!'

        if choice == '1':
            while not username:
                username = raw_input('Username: ')

            while not password:
                password = getpass.getpass('Password: ')

            auth = urllib2.HTTPPasswordMgr()
            host = urlparse.urlparse(self.repository)[1]
            auth.add_password(self.realm, host, username, password)
            (code, result) = self.post_to_server(self.build_post_data('submit'), auth)
            print 'Server response (%s): %s' % (code, result)
            if config == {} and code == 200:
                print 'I can store your PyPI login so future submissions will be faster.'
                print '(the login will be stored in %s)' % self._get_rc_file()
                choice = 'X'
                while choice.lower() not in 'yn':
                    choice = raw_input('Save your login (y/N)?')
                    if not choice:
                        choice = 'n'

                if choice.lower() == 'y':
                    self._store_pypirc(username, password)
        elif choice == '2':
            data = {':action': 'user'}
            data['name'] = data['password'] = data['email'] = ''
            data['confirm'] = None
            while not data['name']:
                data['name'] = raw_input('Username: ')

            while data['password'] != data['confirm']:
                while not data['password']:
                    data['password'] = getpass.getpass('Password: ')

                while not data['confirm']:
                    data['confirm'] = getpass.getpass(' Confirm: ')

                if data['password'] != data['confirm']:
                    data['password'] = ''
                    data['confirm'] = None
                    print "Password and confirm don't match!"

            while not data['email']:
                data['email'] = raw_input('   EMail: ')

            (code, result) = self.post_to_server(data)
            if code != 200:
                print 'Server response (%s): %s' % (code, result)
            else:
                print 'You will receive an email shortly.'
                print 'Follow the instructions in it to complete registration.'
        elif choice == '3':
            data = {':action': 'password_reset'}
            data['email'] = ''
            while not data['email']:
                data['email'] = raw_input('Your email address: ')

            (code, result) = self.post_to_server(data)
            print 'Server response (%s): %s' % (code, result)
        return

    def build_post_data(self, action):
        meta = self.distribution.metadata
        if hasattr(meta, 'get_provides'):
            provides = meta.get_provides()
            requires = meta.get_requires()
            obsoletes = meta.get_obsoletes()
        else:
            provides = []
            requires = []
            obsoletes = []
        data = {':action': action, 'metadata_version': '1.0', 'name': meta.get_name(), 'version': meta.get_version(), 'summary': meta.get_description(), 'home_page': meta.get_url(), 'author': meta.get_contact(), 'author_email': meta.get_contact_email(), 'license': meta.get_licence(), 'description': meta.get_long_description(), 'keywords': meta.get_keywords(), 'platform': meta.get_platforms(), 'classifiers': meta.get_classifiers(), 'download_url': meta.get_download_url(), 'provides': provides, 'requires': requires, 'obsoletes': obsoletes}
        if data['provides'] or data['requires'] or data['obsoletes']:
            data['metadata_version'] = '1.1'
        return data

    def post_to_server(self, data, auth=None):
        """ Post a query to the server, and return a string response.
        """
        self.announce('Registering %s to %s' % (data['name'], self.repository), log.INFO)
        boundary = '--------------GHSKFJDLGDS7543FJKLFHRE75642756743254'
        sep_boundary = '\n--' + boundary
        end_boundary = sep_boundary + '--'
        body = StringIO.StringIO()
        for (key, value) in data.items():
            if type(value) not in (type([]), type(())):
                value = [
                 value]
            for value in value:
                if isinstance(value, str):
                    value = unicode(value, 'utf8')
                value = value.encode('utf-8')
                body.write(sep_boundary)
                body.write('\nContent-Disposition: form-data; name="%s"' % key)
                body.write('\n\n')
                body.write(value)
                if value and value[(-1)] == '\r':
                    body.write('\n')

        body.write(end_boundary)
        body.write('\n')
        body = body.getvalue()
        headers = {'Content-type': 'multipart/form-data; boundary=%s; charset=utf-8' % boundary, 'Content-length': str(len(body))}
        req = urllib2.Request(self.repository, body, headers)
        opener = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(password_mgr=auth))
        data = ''
        try:
            result = opener.open(req)
        except urllib2.HTTPError, e:
            if self.show_response:
                data = e.fp.read()
            result = (
             e.code, e.msg)
        except urllib2.URLError, e:
            result = (
             500, str(e))
        else:
            if self.show_response:
                data = result.read()
            result = (200, 'OK')

        if self.show_response:
            print '-' * 75, data, '-' * 75
        return result