# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/dist/mupload.py
# Compiled at: 2008-03-20 05:18:16
"""distutils.command.upload

Implements the Distutils 'upload' subcommand (upload package to PyPI)."""
from distutils.errors import *
from iw.dist.core import PyPIRCCommand
from distutils.spawn import spawn
from distutils import log
try:
    from hashlib import md5
except ImportError:
    from md5 import md5

import os, socket, platform, ConfigParser, httplib, base64, urlparse, cStringIO as StringIO

class mupload(PyPIRCCommand):
    __module__ = __name__
    description = 'upload binary package to PyPI'
    user_options = [
     (
      'repository=', 'r', 'url of repository [default: %s]' % PyPIRCCommand.DEFAULT_REPOSITORY), ('show-response', None, 'display full response text from server'), ('sign', 's', 'sign files to upload using gpg'), ('identity=', 'i', 'GPG identity used to sign files')]
    boolean_options = [
     'show-response', 'sign']

    def initialize_options(self):
        PyPIRCCommand.initialize_options(self)
        self.username = ''
        self.password = ''
        self.show_response = 0
        self.sign = False
        self.identity = None
        return

    def finalize_options(self):
        PyPIRCCommand.finalize_options(self)
        if self.identity and not self.sign:
            raise DistutilsOptionError('Must use --sign for --identity to have meaning')
        config = self._read_pypirc()
        if config != {}:
            self.username = config['username']
            self.password = config['password']
            self.repository = config['repository']
            self.realm = config['realm']

    def run(self):
        if not self.distribution.dist_files:
            raise DistutilsOptionError('No dist file created in earlier command')
        for (command, pyversion, filename) in self.distribution.dist_files:
            self.upload_file(command, pyversion, filename)

    def upload_file(self, command, pyversion, filename):
        if self.sign:
            gpg_args = [
             'gpg', '--detach-sign', '-a', filename]
            if self.identity:
                gpg_args[2:2] = [
                 '--local-user', self.identity]
            spawn(gpg_args, dry_run=self.dry_run)
        content = open(filename, 'rb').read()
        meta = self.distribution.metadata
        data = {':action': 'file_upload', 'protcol_version': '1', 'name': meta.get_name(), 'version': meta.get_version(), 'content': (os.path.basename(filename), content), 'filetype': command, 'pyversion': pyversion, 'md5_digest': md5(content).hexdigest(), 'metadata_version': '1.0', 'summary': meta.get_description(), 'home_page': meta.get_url(), 'author': meta.get_contact(), 'author_email': meta.get_contact_email(), 'license': meta.get_licence(), 'description': meta.get_long_description(), 'keywords': meta.get_keywords(), 'platform': meta.get_platforms(), 'classifiers': meta.get_classifiers(), 'download_url': meta.get_download_url()}
        if hasattr(meta, 'get_provides'):
            data['provides'] = meta.get_provides()
            data['requires'] = meta.get_requires()
            data['obsoletes'] = meta.get_obsoletes()
        comment = ''
        if command == 'bdist_rpm':
            (dist, version, id) = platform.dist()
            if dist:
                comment = 'built for %s %s' % (dist, version)
        elif command == 'bdist_dumb':
            comment = 'built for %s' % platform.platform(terse=1)
        data['comment'] = comment
        if self.sign:
            data['gpg_signature'] = (
             os.path.basename(filename) + '.asc', open(filename + '.asc').read())
        auth = 'Basic ' + base64.encodestring(self.username + ':' + self.password).strip()
        boundary = '--------------GHSKFJDLGDS7543FJKLFHRE75642756743254'
        sep_boundary = '\n--' + boundary
        end_boundary = sep_boundary + '--'
        body = StringIO.StringIO()
        for (key, value) in data.items():
            if type(value) != type([]):
                value = [
                 value]
            for value in value:
                if type(value) is tuple:
                    fn = ';filename="%s"' % value[0]
                    value = value[1]
                else:
                    fn = ''
                value = str(value)
                body.write(sep_boundary)
                body.write('\nContent-Disposition: form-data; name="%s"' % key)
                body.write(fn)
                body.write('\n\n')
                body.write(value)
                if value and value[(-1)] == '\r':
                    body.write('\n')

        body.write(end_boundary)
        body.write('\n')
        body = body.getvalue()
        self.announce('Submitting %s to %s' % (filename, self.repository), log.INFO)
        (schema, netloc, url, params, query, fragments) = urlparse.urlparse(self.repository)
        assert not params and not query and not fragments
        if schema == 'http':
            http = httplib.HTTPConnection(netloc)
        elif schema == 'https':
            http = httplib.HTTPSConnection(netloc)
        else:
            raise AssertionError, 'unsupported schema ' + schema
        data = ''
        loglevel = log.INFO
        try:
            http.connect()
            http.putrequest('POST', url)
            http.putheader('Content-type', 'multipart/form-data; boundary=%s' % boundary)
            http.putheader('Content-length', str(len(body)))
            http.putheader('Authorization', auth)
            http.endheaders()
            http.send(body)
        except socket.error, e:
            self.announce(str(e), log.ERROR)
            return

        r = http.getresponse()
        if r.status == 200:
            self.announce('Server response (%s): %s' % (r.status, r.reason), log.INFO)
        else:
            self.announce('Upload failed (%s): %s' % (r.status, r.reason), log.ERROR)
        if self.show_response:
            print '-' * 75, r.read(), '-' * 75