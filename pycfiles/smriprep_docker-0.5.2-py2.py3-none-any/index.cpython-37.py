# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pn36swhz/pip/pip/_vendor/distlib/index.py
# Compiled at: 2020-02-14 17:24:54
# Size of source mod 2**32: 21066 bytes
import hashlib, logging, os, shutil, subprocess, tempfile
try:
    from threading import Thread
except ImportError:
    from dummy_threading import Thread

from . import DistlibException
from .compat import HTTPBasicAuthHandler, Request, HTTPPasswordMgr, urlparse, build_opener, string_types
from .util import cached_property, zip_dir, ServerProxy
logger = logging.getLogger(__name__)
DEFAULT_INDEX = 'https://pypi.org/pypi'
DEFAULT_REALM = 'pypi'

class PackageIndex(object):
    __doc__ = '\n    This class represents a package index compatible with PyPI, the Python\n    Package Index.\n    '
    boundary = b'----------ThIs_Is_tHe_distlib_index_bouNdaRY_$'

    def __init__--- This code section failed: ---

 L.  43         0  LOAD_FAST                'url'
                2  JUMP_IF_TRUE_OR_POP     6  'to 6'
                4  LOAD_GLOBAL              DEFAULT_INDEX
              6_0  COME_FROM             2  '2'
                6  LOAD_FAST                'self'
                8  STORE_ATTR               url

 L.  44        10  LOAD_FAST                'self'
               12  LOAD_METHOD              read_configuration
               14  CALL_METHOD_0         0  '0 positional arguments'
               16  POP_TOP          

 L.  45        18  LOAD_GLOBAL              urlparse
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                url
               24  CALL_FUNCTION_1       1  '1 positional argument'
               26  UNPACK_SEQUENCE_6     6 
               28  STORE_FAST               'scheme'
               30  STORE_FAST               'netloc'
               32  STORE_FAST               'path'
               34  STORE_FAST               'params'
               36  STORE_FAST               'query'
               38  STORE_FAST               'frag'

 L.  46        40  LOAD_FAST                'params'
               42  POP_JUMP_IF_TRUE     60  'to 60'
               44  LOAD_FAST                'query'
               46  POP_JUMP_IF_TRUE     60  'to 60'
               48  LOAD_FAST                'frag'
               50  POP_JUMP_IF_TRUE     60  'to 60'
               52  LOAD_FAST                'scheme'
               54  LOAD_CONST               ('http', 'https')
               56  COMPARE_OP               not-in
               58  POP_JUMP_IF_FALSE    74  'to 74'
             60_0  COME_FROM            50  '50'
             60_1  COME_FROM            46  '46'
             60_2  COME_FROM            42  '42'

 L.  47        60  LOAD_GLOBAL              DistlibException
               62  LOAD_STR                 'invalid repository: %s'
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                url
               68  BINARY_MODULO    
               70  CALL_FUNCTION_1       1  '1 positional argument'
               72  RAISE_VARARGS_1       1  'exception instance'
             74_0  COME_FROM            58  '58'

 L.  48        74  LOAD_CONST               None
               76  LOAD_FAST                'self'
               78  STORE_ATTR               password_handler

 L.  49        80  LOAD_CONST               None
               82  LOAD_FAST                'self'
               84  STORE_ATTR               ssl_verifier

 L.  50        86  LOAD_CONST               None
               88  LOAD_FAST                'self'
               90  STORE_ATTR               gpg

 L.  51        92  LOAD_CONST               None
               94  LOAD_FAST                'self'
               96  STORE_ATTR               gpg_home

 L.  52        98  LOAD_GLOBAL              open
              100  LOAD_GLOBAL              os
              102  LOAD_ATTR                devnull
              104  LOAD_STR                 'w'
              106  CALL_FUNCTION_2       2  '2 positional arguments'
              108  SETUP_WITH          192  'to 192'
              110  STORE_FAST               'sink'

 L.  55       112  SETUP_LOOP          188  'to 188'
              114  LOAD_CONST               ('gpg', 'gpg2')
              116  GET_ITER         
              118  FOR_ITER            186  'to 186'
              120  STORE_FAST               's'

 L.  56       122  SETUP_EXCEPT        164  'to 164'

 L.  57       124  LOAD_GLOBAL              subprocess
              126  LOAD_ATTR                check_call
              128  LOAD_FAST                's'
              130  LOAD_STR                 '--version'
              132  BUILD_LIST_2          2 
              134  LOAD_FAST                'sink'

 L.  58       136  LOAD_FAST                'sink'
              138  LOAD_CONST               ('stdout', 'stderr')
              140  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              142  STORE_FAST               'rc'

 L.  59       144  LOAD_FAST                'rc'
              146  LOAD_CONST               0
              148  COMPARE_OP               ==
              150  POP_JUMP_IF_FALSE   160  'to 160'

 L.  60       152  LOAD_FAST                's'
              154  LOAD_FAST                'self'
              156  STORE_ATTR               gpg

 L.  61       158  BREAK_LOOP       
            160_0  COME_FROM           150  '150'
              160  POP_BLOCK        
              162  JUMP_BACK           118  'to 118'
            164_0  COME_FROM_EXCEPT    122  '122'

 L.  62       164  DUP_TOP          
              166  LOAD_GLOBAL              OSError
              168  COMPARE_OP               exception-match
              170  POP_JUMP_IF_FALSE   182  'to 182'
              172  POP_TOP          
              174  POP_TOP          
              176  POP_TOP          

 L.  63       178  POP_EXCEPT       
              180  JUMP_BACK           118  'to 118'
            182_0  COME_FROM           170  '170'
              182  END_FINALLY      
              184  JUMP_BACK           118  'to 118'
              186  POP_BLOCK        
            188_0  COME_FROM_LOOP      112  '112'
              188  POP_BLOCK        
              190  LOAD_CONST               None
            192_0  COME_FROM_WITH      108  '108'
              192  WITH_CLEANUP_START
              194  WITH_CLEANUP_FINISH
              196  END_FINALLY      

Parse error at or near `COME_FROM' instruction at offset 74_0

    def _get_pypirc_command(self):
        """
        Get the distutils command for interacting with PyPI configurations.
        :return: the command.
        """
        from distutils.core import Distribution
        from distutils.config import PyPIRCCommand
        d = Distribution()
        return PyPIRCCommand(d)

    def read_configuration(self):
        """
        Read the PyPI access configuration as supported by distutils, getting
        PyPI to do the actual work. This populates ``username``, ``password``,
        ``realm`` and ``url`` attributes from the configuration.
        """
        c = self._get_pypirc_command
        c.repository = self.url
        cfg = c._read_pypirc
        self.username = cfg.get('username')
        self.password = cfg.get('password')
        self.realm = cfg.get('realm', 'pypi')
        self.url = cfg.get('repository', self.url)

    def save_configuration(self):
        """
        Save the PyPI access configuration. You must have set ``username`` and
        ``password`` attributes before calling this method.

        Again, distutils is used to do the actual work.
        """
        self.check_credentials
        c = self._get_pypirc_command
        c._store_pypirc(self.username, self.password)

    def check_credentials(self):
        """
        Check that ``username`` and ``password`` have been set, and raise an
        exception if not.
        """
        if self.username is None or self.password is None:
            raise DistlibException('username and password must be set')
        pm = HTTPPasswordMgr()
        _, netloc, _, _, _, _ = urlparse(self.url)
        pm.add_password(self.realm, netloc, self.username, self.password)
        self.password_handler = HTTPBasicAuthHandler(pm)

    def register(self, metadata):
        """
        Register a distribution on PyPI, using the provided metadata.

        :param metadata: A :class:`Metadata` instance defining at least a name
                         and version number for the distribution to be
                         registered.
        :return: The HTTP response received from PyPI upon submission of the
                request.
        """
        self.check_credentials
        metadata.validate
        d = metadata.todict
        d[':action'] = 'verify'
        request = self.encode_request(d.items, [])
        response = self.send_request(request)
        d[':action'] = 'submit'
        request = self.encode_request(d.items, [])
        return self.send_request(request)

    def _reader(self, name, stream, outbuf):
        """
        Thread runner for reading lines of from a subprocess into a buffer.

        :param name: The logical name of the stream (used for logging only).
        :param stream: The stream to read from. This will typically a pipe
                       connected to the output stream of a subprocess.
        :param outbuf: The list to append the read lines to.
        """
        while True:
            s = stream.readline
            if not s:
                break
            s = s.decode('utf-8').rstrip
            outbuf.append(s)
            logger.debug('%s: %s' % (name, s))

        stream.close

    def get_sign_command(self, filename, signer, sign_password, keystore=None):
        """
        Return a suitable command for signing a file.

        :param filename: The pathname to the file to be signed.
        :param signer: The identifier of the signer of the file.
        :param sign_password: The passphrase for the signer's
                              private key used for signing.
        :param keystore: The path to a directory which contains the keys
                         used in verification. If not specified, the
                         instance's ``gpg_home`` attribute is used instead.
        :return: The signing command as a list suitable to be
                 passed to :class:`subprocess.Popen`.
        """
        cmd = [
         self.gpg, '--status-fd', '2', '--no-tty']
        if keystore is None:
            keystore = self.gpg_home
        if keystore:
            cmd.extend(['--homedir', keystore])
        if sign_password is not None:
            cmd.extend(['--batch', '--passphrase-fd', '0'])
        td = tempfile.mkdtemp
        sf = os.path.join(td, os.path.basename(filename) + '.asc')
        cmd.extend(['--detach-sign', '--armor', '--local-user',
         signer, '--output', sf, filename])
        logger.debug('invoking: %s', ' '.join(cmd))
        return (cmd, sf)

    def run_command(self, cmd, input_data=None):
        """
        Run a command in a child process , passing it any input data specified.

        :param cmd: The command to run.
        :param input_data: If specified, this must be a byte string containing
                           data to be sent to the child process.
        :return: A tuple consisting of the subprocess' exit code, a list of
                 lines read from the subprocess' ``stdout``, and a list of
                 lines read from the subprocess' ``stderr``.
        """
        kwargs = {'stdout':subprocess.PIPE, 
         'stderr':subprocess.PIPE}
        if input_data is not None:
            kwargs['stdin'] = subprocess.PIPE
        stdout = []
        stderr = []
        p = (subprocess.Popen)(cmd, **kwargs)
        t1 = Thread(target=(self._reader), args=('stdout', p.stdout, stdout))
        t1.start
        t2 = Thread(target=(self._reader), args=('stderr', p.stderr, stderr))
        t2.start
        if input_data is not None:
            p.stdin.write(input_data)
            p.stdin.close
        p.wait
        t1.join
        t2.join
        return (p.returncode, stdout, stderr)

    def sign_file(self, filename, signer, sign_password, keystore=None):
        """
        Sign a file.

        :param filename: The pathname to the file to be signed.
        :param signer: The identifier of the signer of the file.
        :param sign_password: The passphrase for the signer's
                              private key used for signing.
        :param keystore: The path to a directory which contains the keys
                         used in signing. If not specified, the instance's
                         ``gpg_home`` attribute is used instead.
        :return: The absolute pathname of the file where the signature is
                 stored.
        """
        cmd, sig_file = self.get_sign_command(filename, signer, sign_password, keystore)
        rc, stdout, stderr = self.run_command(cmd, sign_password.encode('utf-8'))
        if rc != 0:
            raise DistlibException('sign command failed with error code %s' % rc)
        return sig_file

    def upload_file(self, metadata, filename, signer=None, sign_password=None, filetype='sdist', pyversion='source', keystore=None):
        """
        Upload a release file to the index.

        :param metadata: A :class:`Metadata` instance defining at least a name
                         and version number for the file to be uploaded.
        :param filename: The pathname of the file to be uploaded.
        :param signer: The identifier of the signer of the file.
        :param sign_password: The passphrase for the signer's
                              private key used for signing.
        :param filetype: The type of the file being uploaded. This is the
                        distutils command which produced that file, e.g.
                        ``sdist`` or ``bdist_wheel``.
        :param pyversion: The version of Python which the release relates
                          to. For code compatible with any Python, this would
                          be ``source``, otherwise it would be e.g. ``3.2``.
        :param keystore: The path to a directory which contains the keys
                         used in signing. If not specified, the instance's
                         ``gpg_home`` attribute is used instead.
        :return: The HTTP response received from PyPI upon submission of the
                request.
        """
        self.check_credentials
        if not os.path.exists(filename):
            raise DistlibException('not found: %s' % filename)
        else:
            metadata.validate
            d = metadata.todict
            sig_file = None
            if signer:
                if not self.gpg:
                    logger.warning('no signing program available - not signed')
                else:
                    sig_file = self.sign_file(filename, signer, sign_password, keystore)
        with openfilename'rb' as (f):
            file_data = f.read
        md5_digest = hashlib.md5(file_data).hexdigest
        sha256_digest = hashlib.sha256(file_data).hexdigest
        d.update({':action':'file_upload', 
         'protocol_version':'1', 
         'filetype':filetype, 
         'pyversion':pyversion, 
         'md5_digest':md5_digest, 
         'sha256_digest':sha256_digest})
        files = [
         (
          'content', os.path.basename(filename), file_data)]
        if sig_file:
            with opensig_file'rb' as (f):
                sig_data = f.read
            files.append(('gpg_signature', os.path.basename(sig_file),
             sig_data))
            shutil.rmtree(os.path.dirname(sig_file))
        request = self.encode_request(d.items, files)
        return self.send_request(request)

    def upload_documentation(self, metadata, doc_dir):
        """
        Upload documentation to the index.

        :param metadata: A :class:`Metadata` instance defining at least a name
                         and version number for the documentation to be
                         uploaded.
        :param doc_dir: The pathname of the directory which contains the
                        documentation. This should be the directory that
                        contains the ``index.html`` for the documentation.
        :return: The HTTP response received from PyPI upon submission of the
                request.
        """
        self.check_credentials
        if not os.path.isdir(doc_dir):
            raise DistlibException('not a directory: %r' % doc_dir)
        fn = os.path.join(doc_dir, 'index.html')
        if not os.path.exists(fn):
            raise DistlibException('not found: %r' % fn)
        metadata.validate
        name, version = metadata.name, metadata.version
        zip_data = zip_dir(doc_dir).getvalue
        fields = [(':action', 'doc_upload'),
         (
          'name', name), ('version', version)]
        files = [('content', name, zip_data)]
        request = self.encode_request(fields, files)
        return self.send_request(request)

    def get_verify_command(self, signature_filename, data_filename, keystore=None):
        """
        Return a suitable command for verifying a file.

        :param signature_filename: The pathname to the file containing the
                                   signature.
        :param data_filename: The pathname to the file containing the
                              signed data.
        :param keystore: The path to a directory which contains the keys
                         used in verification. If not specified, the
                         instance's ``gpg_home`` attribute is used instead.
        :return: The verifying command as a list suitable to be
                 passed to :class:`subprocess.Popen`.
        """
        cmd = [
         self.gpg, '--status-fd', '2', '--no-tty']
        if keystore is None:
            keystore = self.gpg_home
        if keystore:
            cmd.extend(['--homedir', keystore])
        cmd.extend(['--verify', signature_filename, data_filename])
        logger.debug('invoking: %s', ' '.join(cmd))
        return cmd

    def verify_signature(self, signature_filename, data_filename, keystore=None):
        """
        Verify a signature for a file.

        :param signature_filename: The pathname to the file containing the
                                   signature.
        :param data_filename: The pathname to the file containing the
                              signed data.
        :param keystore: The path to a directory which contains the keys
                         used in verification. If not specified, the
                         instance's ``gpg_home`` attribute is used instead.
        :return: True if the signature was verified, else False.
        """
        if not self.gpg:
            raise DistlibException('verification unavailable because gpg unavailable')
        cmd = self.get_verify_command(signature_filename, data_filename, keystore)
        rc, stdout, stderr = self.run_command(cmd)
        if rc not in (0, 1):
            raise DistlibException('verify command failed with error code %s' % rc)
        return rc == 0

    def download_file(self, url, destfile, digest=None, reporthook=None):
        """
        This is a convenience method for downloading a file from an URL.
        Normally, this will be a file from the index, though currently
        no check is made for this (i.e. a file can be downloaded from
        anywhere).

        The method is just like the :func:`urlretrieve` function in the
        standard library, except that it allows digest computation to be
        done during download and checking that the downloaded data
        matched any expected value.

        :param url: The URL of the file to be downloaded (assumed to be
                    available via an HTTP GET request).
        :param destfile: The pathname where the downloaded file is to be
                         saved.
        :param digest: If specified, this must be a (hasher, value)
                       tuple, where hasher is the algorithm used (e.g.
                       ``'md5'``) and ``value`` is the expected value.
        :param reporthook: The same as for :func:`urlretrieve` in the
                           standard library.
        """
        if digest is None:
            digester = None
            logger.debug('No digest specified')
        else:
            if isinstancedigest(list, tuple):
                hasher, digest = digest
            else:
                hasher = 'md5'
            digester = getattrhashlibhasher()
            logger.debug('Digest specified: %s' % digest)
        with opendestfile'wb' as (dfp):
            sfp = self.send_request(Request(url))
            try:
                headers = sfp.info
                blocksize = 8192
                size = -1
                read = 0
                blocknum = 0
                if 'content-length' in headers:
                    size = int(headers['Content-Length'])
                if reporthook:
                    reporthook(blocknum, blocksize, size)
                while 1:
                    block = sfp.read(blocksize)
                    if not block:
                        break
                    read += len(block)
                    dfp.write(block)
                    if digester:
                        digester.update(block)
                    blocknum += 1
                    if reporthook:
                        reporthook(blocknum, blocksize, size)

            finally:
                sfp.close

        if size >= 0:
            if read < size:
                raise DistlibException('retrieval incomplete: got only %d out of %d bytes' % (
                 read, size))
        if digester:
            actual = digester.hexdigest
            if digest != actual:
                raise DistlibException('%s digest mismatch for %s: expected %s, got %s' % (
                 hasher, destfile,
                 digest, actual))
            logger.debug('Digest verified: %s', digest)

    def send_request(self, req):
        """
        Send a standard library :class:`Request` to PyPI and return its
        response.

        :param req: The request to send.
        :return: The HTTP response from PyPI (a standard library HTTPResponse).
        """
        handlers = []
        if self.password_handler:
            handlers.append(self.password_handler)
        if self.ssl_verifier:
            handlers.append(self.ssl_verifier)
        opener = build_opener(*handlers)
        return opener.open(req)

    def encode_request(self, fields, files):
        """
        Encode fields and files for posting to an HTTP server.

        :param fields: The fields to send as a list of (fieldname, value)
                       tuples.
        :param files: The files to send as a list of (fieldname, filename,
                      file_bytes) tuple.
        """
        parts = []
        boundary = self.boundary
        for k, values in fields:
            if not isinstancevalues(list, tuple):
                values = [
                 values]
            for v in values:
                parts.extend((
                 b'--' + boundary,
                 ('Content-Disposition: form-data; name="%s"' % k).encode('utf-8'),
                 b'',
                 v.encode('utf-8')))

        for key, filename, value in files:
            parts.extend((
             b'--' + boundary,
             ('Content-Disposition: form-data; name="%s"; filename="%s"' % (
              key, filename)).encode('utf-8'),
             b'',
             value))

        parts.extend((b'--' + boundary + b'--', b''))
        body = (b'\r\n').join(parts)
        ct = b'multipart/form-data; boundary=' + boundary
        headers = {'Content-type':ct, 
         'Content-length':str(len(body))}
        return Request(self.url, body, headers)

    def search(self, terms, operator=None):
        if isinstancetermsstring_types:
            terms = {'name': terms}
        rpc_proxy = ServerProxy((self.url), timeout=3.0)
        try:
            return rpc_proxy.search(terms, operator or 'and')
        finally:
            rpc_proxy('close')()