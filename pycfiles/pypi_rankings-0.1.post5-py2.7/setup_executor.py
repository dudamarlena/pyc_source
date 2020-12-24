# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/pypi_rankings/crawlers/setup_executor.py
# Compiled at: 2015-02-17 04:35:44
import types, setuptools, distutils.core, mock, os, sys, shutil, subprocess
required = None

def setup_mock(*args, **kwargs):
    global required
    required = kwargs.get('install_requires', [])
    if required is None:
        required = []
    if isinstance(required, (set, tuple, types.GeneratorType, dict)):
        required = list(required)
    if isinstance(required, basestring):
        required = required.strip().split('\n')
    if not isinstance(required, list):
        required = None
    return


with mock.patch.object(setuptools, 'setup', setup_mock):
    with mock.patch.object(distutils.core, 'setup', setup_mock):
        with mock.patch.object(sys, 'exit'):
            with mock.patch.object(os, '_exit'):
                with mock.patch.object(os, 'system'):
                    with mock.patch.object(os, 'rename'):
                        with mock.patch.object(os, 'remove'):
                            with mock.patch.object(os, 'mkdir'):
                                with mock.patch.object(os, 'makedirs'):
                                    with mock.patch.object(shutil, 'rmtree'):
                                        with mock.patch.object(shutil, 'move'):
                                            with mock.patch.object(shutil, 'copy'):
                                                with mock.patch.object(shutil, 'copyfile'):
                                                    with mock.patch.object(subprocess, 'Popen'):
                                                        execfile('setup.py')
print
print repr(required)