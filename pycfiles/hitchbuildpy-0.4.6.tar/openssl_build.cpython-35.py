# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colm/hitch/buildpy/hitchbuildpy/openssl_build.py
# Compiled at: 2018-09-20 06:24:02
# Size of source mod 2**32: 1506 bytes
from commandlib import CommandPath, Command
from distutils.version import LooseVersion
from path import Path
from hitchbuildpy import utils
import hitchbuild

class OpenSSL(hitchbuild.HitchBuild):

    def __init__(self, version):
        self.version = version

    @property
    def basepath(self):
        return self.build_path / 'openssl{0}'.format(self.version)

    def fingerprint(self):
        return str(hash(self.version))

    def clean(self):
        self.basepath.rmtree(ignore_errors=True)

    @property
    def full_directory(self):
        return self.basepath / 'openssl-1.1.1'

    def build(self):
        if not self.basepath.exists() or self.last_run_had_exception:
            self.basepath.rmtree(ignore_errors=True)
            self.basepath.mkdir()
            download_to = self.basepath / 'openssl-1.1.1.tar.gz'
            utils.download_file(download_to, 'https://www.openssl.org/source/openssl-1.1.1.tar.gz')
            utils.extract_archive(download_to, self.basepath)
            print('Running ./configure --prefix={}'.format(self.full_directory))
            try:
                Command('./configure')('--prefix={}'.format(self.full_directory)).in_dir(self.full_directory).run()
            except:
                print('error')
                import IPython
                IPython.embed()

            import IPython
            IPython.embed()
        self.verify()

    def verify(self):
        pass