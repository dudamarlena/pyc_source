# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jason/workspace/pycapnp/buildutils/build.py
# Compiled at: 2015-04-13 17:55:55
"""Build the bundled capnp distribution"""
import subprocess, os, tempfile

def build_libcapnp(bundle_dir, build_dir, verbose=False):
    bundle_dir = os.path.abspath(bundle_dir)
    capnp_dir = os.path.join(bundle_dir, 'capnproto-c++')
    build_dir = os.path.abspath(build_dir)
    with tempfile.TemporaryFile() as (f):
        stdout = f
        if verbose:
            stdout = None
        cxxflags = os.environ.get('CXXFLAGS', None)
        os.environ['CXXFLAGS'] = (cxxflags or '') + ' -fPIC -O2 -DNDEBUG'
        conf = subprocess.Popen(['./configure', '--disable-shared', '--prefix', build_dir], cwd=capnp_dir, stdout=stdout)
        returncode = conf.wait()
        if returncode != 0:
            raise RuntimeError('Configure failed')
        make = subprocess.Popen(['make', '-j4', 'install'], cwd=capnp_dir, stdout=stdout)
        returncode = make.wait()
        if cxxflags is None:
            del os.environ['CXXFLAGS']
        else:
            os.environ['CXXFLAGS'] = cxxflags
        if returncode != 0:
            raise RuntimeError('Make failed')
    return