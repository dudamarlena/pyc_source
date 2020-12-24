# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/wheel/wheel/wheelfile.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 7298 bytes
from __future__ import print_function
import csv, hashlib, os.path, re, stat, time
from collections import OrderedDict
from distutils import log as logger
from zipfile import ZIP_DEFLATED, ZipInfo, ZipFile
from wheel.cli import WheelError
from wheel.util import urlsafe_b64decode, as_unicode, native, urlsafe_b64encode, as_bytes, StringIO
WHEEL_INFO_RE = re.compile('^(?P<namever>(?P<name>.+?)-(?P<ver>.+?))(-(?P<build>\\d[^-]*))?\n     -(?P<pyver>.+?)-(?P<abi>.+?)-(?P<plat>.+?)\\.whl$', re.VERBOSE)

def get_zipinfo_datetime(timestamp=None):
    timestamp = int(os.environ.get('SOURCE_DATE_EPOCH', timestamp or time.time()))
    return time.gmtime(timestamp)[0:6]


class WheelFile(ZipFile):
    __doc__ = 'A ZipFile derivative class that also reads SHA-256 hashes from\n    .dist-info/RECORD and checks any read files against those.\n    '
    _default_algorithm = hashlib.sha256

    def __init__(self, file, mode='r', compression=ZIP_DEFLATED):
        basename = os.path.basename(file)
        self.parsed_filename = WHEEL_INFO_RE.match(basename)
        if not basename.endswith('.whl') or self.parsed_filename is None:
            raise WheelError('Bad wheel filename {!r}'.format(basename))
        ZipFile.__init__(self, file, mode, compression=compression, allowZip64=True)
        self.dist_info_path = '{}.dist-info'.format(self.parsed_filename.group('namever'))
        self.record_path = self.dist_info_path + '/RECORD'
        self._file_hashes = OrderedDict()
        self._file_sizes = {}
        if mode == 'r':
            self._file_hashes[self.record_path] = (None, None)
            self._file_hashes[self.record_path + '.jws'] = (None, None)
            self._file_hashes[self.record_path + '.p7s'] = (None, None)
            try:
                record = self.open(self.record_path)
            except KeyError:
                raise WheelError('Missing {} file'.format(self.record_path))

            with record:
                for line in record:
                    line = line.decode('utf-8')
                    path, hash_sum, size = line.rsplit(',', 2)
                    if hash_sum:
                        algorithm, hash_sum = hash_sum.split('=')
                        try:
                            hashlib.new(algorithm)
                        except ValueError:
                            raise WheelError('Unsupported hash algorithm: {}'.format(algorithm))

                        if algorithm.lower() in {'md5', 'sha1'}:
                            raise WheelError('Weak hash algorithm ({}) is not permitted by PEP 427'.format(algorithm))
                        self._file_hashes[path] = (
                         algorithm, urlsafe_b64decode(hash_sum.encode('ascii')))

    def open(self, name_or_info, mode='r', pwd=None):

        def _update_crc(newdata, eof=None):
            if eof is None:
                eof = ef._eof
                update_crc_orig(newdata)
            else:
                update_crc_orig(newdata, eof)
            running_hash.update(newdata)
            if eof:
                if running_hash.digest() != expected_hash:
                    raise WheelError("Hash mismatch for file '{}'".format(native(ef_name)))

        ef = ZipFile.open(self, name_or_info, mode, pwd)
        ef_name = as_unicode(name_or_info.filename if isinstance(name_or_info, ZipInfo) else name_or_info)
        if mode == 'r':
            if not ef_name.endswith('/'):
                if ef_name not in self._file_hashes:
                    raise WheelError("No hash found for file '{}'".format(native(ef_name)))
                algorithm, expected_hash = self._file_hashes[ef_name]
                if expected_hash is not None:
                    running_hash = hashlib.new(algorithm)
                    update_crc_orig, ef._update_crc = ef._update_crc, _update_crc
        return ef

    def write_files(self, base_dir):
        logger.info("creating '%s' and adding '%s' to it", self.filename, base_dir)
        deferred = []
        for root, dirnames, filenames in os.walk(base_dir):
            dirnames.sort()
            for name in sorted(filenames):
                path = os.path.normpath(os.path.join(root, name))
                if os.path.isfile(path):
                    arcname = os.path.relpath(path, base_dir).replace(os.path.sep, '/')
                    if arcname == self.record_path:
                        continue
                    if root.endswith('.dist-info'):
                        deferred.append((path, arcname))
                    else:
                        self.write(path, arcname)

        deferred.sort()
        for path, arcname in deferred:
            self.write(path, arcname)

    def write(self, filename, arcname=None, compress_type=None):
        with open(filename, 'rb') as (f):
            st = os.fstat(f.fileno())
            data = f.read()
        zinfo = ZipInfo((arcname or filename), date_time=(get_zipinfo_datetime(st.st_mtime)))
        zinfo.external_attr = (stat.S_IMODE(st.st_mode) | stat.S_IFMT(st.st_mode)) << 16
        zinfo.compress_type = compress_type or self.compression
        self.writestr(zinfo, data, compress_type)

    def writestr(self, zinfo_or_arcname, bytes, compress_type=None):
        ZipFile.writestr(self, zinfo_or_arcname, bytes, compress_type)
        fname = zinfo_or_arcname.filename if isinstance(zinfo_or_arcname, ZipInfo) else zinfo_or_arcname
        logger.info("adding '%s'", fname)
        if fname != self.record_path:
            hash_ = self._default_algorithm(bytes)
            self._file_hashes[fname] = (hash_.name, native(urlsafe_b64encode(hash_.digest())))
            self._file_sizes[fname] = len(bytes)

    def close(self):
        if self.fp is not None:
            if self.mode == 'w':
                if self._file_hashes:
                    data = StringIO()
                    writer = csv.writer(data, delimiter=',', quotechar='"', lineterminator='\n')
                    writer.writerows(((fname, algorithm + '=' + hash_, self._file_sizes[fname]) for fname, (algorithm, hash_) in self._file_hashes.items()))
                    writer.writerow((format(self.record_path), '', ''))
                    zinfo = ZipInfo((native(self.record_path)), date_time=(get_zipinfo_datetime()))
                    zinfo.compress_type = self.compression
                    zinfo.external_attr = 28573696
                    self.writestr(zinfo, as_bytes(data.getvalue()))
        ZipFile.close(self)