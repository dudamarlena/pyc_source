# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymatlab/sessionfactory.py
# Compiled at: 2013-10-24 08:37:24
__doc__ = '\nCopyright 2010-2013 Joakim Möller\n\nThis file is part of pymatlab.\n\npymatlab is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\npymatlab is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with pymatlab.  If not, see <http://www.gnu.org/licenses/>.\n'
import os, os.path, platform
from pymatlab.matlab import MatlabSession

def session_factory(options='', output_buffer_size=8096):
    system = platform.system()
    path = None
    if system == 'Linux' or system == 'Darwin':
        locations = os.environ.get('PATH').split(os.pathsep)
        for location in locations:
            candidate = os.path.join(location, 'matlab')
            if os.path.isfile(candidate):
                path = candidate
                break

        executable = os.path.realpath(path)
        basedir = os.path.dirname(os.path.dirname(executable))
        exec_and_options = (' ').join([executable, options])
        session = MatlabSession(basedir, exec_and_options, output_buffer_size)
    elif system == 'Windows':
        locations = os.environ.get('PATH').split(os.pathsep)
        for location in locations:
            candidate = os.path.join(location, 'matlab.exe')
            if os.path.isfile(candidate):
                path = candidate
                break

        executable = os.path.realpath(path)
        basedir = os.path.dirname(os.path.dirname(executable))
        session = MatlabSession(path=basedir, bufsize=output_buffer_size)
    else:
        raise NotSupportedException(('Not supported on the {platform}-platform').format(platform=system))
    return session


def remote_session_factory(hostname, remote_path):
    system = platform.system()
    path = None
    if system == 'Linux' or system == 'Darwin':
        locations = os.environ.get('PATH').split(os.pathsep)
        for location in locations:
            candidate = os.path.join(location, 'matlab')
            if os.path.isfile(candidate):
                path = candidate
                break

        executable = os.path.realpath(path)
        basedir = os.path.dirname(os.path.dirname(executable))
        session = MatlabSession(basedir, ("ssh {host} '/bin/csh -c {full_path}'").format(host=hostname, full_path=remote_path))
    else:
        raise NotSupportedException(('Not supported on the {platform}-platform').format(platform=system))
    return session