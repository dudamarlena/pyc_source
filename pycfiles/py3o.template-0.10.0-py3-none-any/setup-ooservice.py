# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ooservice/setup-ooservice.py
# Compiled at: 2013-11-20 05:57:33
from distutils.core import setup
from distutils.core import Command
import os, glob, sys, py2exe
dist_dir = 'dist\\py3o.openoffice.service'
include_modules = [
 '_winreg', 'win32com', 'win32service',
 'win32serviceutil',
 'win32event']
include_packages = [
 'encodings']
options = dict()
dll_excludes = list()
excludes = []

def __removedirs(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))

        for name in dirs:
            os.rmdir(os.path.join(root, name))

    if os.path.exists(top):
        os.rmdir(top)


def __removefiles(top, suffix):
    for root, dirs, files in os.walk(top):
        for name in files:
            if name.endswith(suffix):
                os.remove(os.path.join(root, name))


if 'clean' in sys.argv:
    top = os.getcwd()
    __removedirs(os.path.join(top, dist_dir))
    __removedirs(os.path.join(top, 'build'))
    __removefiles(top, 'pyc')
if len(sys.argv) == 1:
    sys.argv.append('py2exe')
    sys.argv.append('-q')

class Target:

    def __init__(self, **kw):
        self.__dict__.update(kw)
        self.company_name = ''
        self.copyright = 'Florent AIDE 2010'
        self.name = 'py3o.ooservice'


class MyCommand(Command):
    depend_files = []

    def need_build(self, file):
        for dep_file in self.depend_files:
            if newer(dep_file, file):
                return True


class NSI(MyCommand):
    user_options = [
     ('version', 'V', 'Set version')]

    def initialize_options(self):
        self.version = VERSION

    def finalize_options(self):
        pass

    def need_py2exe(self):
        return True

    def run(self):
        call_args = [
         MAKENSIS_EXECUTABLE, '/DVersion=%s' % VERSION, NSI_FILE]
        Popen(args=call_args)


manifest_template = '\n<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">\n<assemblyIdentity\n    version="5.0.0.0"\n    processorArchitecture="x86"\n    name="%(prog)s"\n    type="win32"\n/>\n<description>%(prog)s Program</description>\n<dependency>\n    <dependentAssembly>\n        <assemblyIdentity\n            type="win32"\n            name="Microsoft.Windows.Common-Controls"\n            version="6.0.0.0"\n            processorArchitecture="X86"\n            publicKeyToken="6595b64144ccf1df"\n            language="*"\n        />\n    </dependentAssembly>\n</dependency>\n</assembly>\n'
RT_MANIFEST = 24
py3o_openofficeservice = Target(description='Open Office headless as a windows service', modules=[
 'ooservice'], create_exe=True, create_dll=True, icon_resources=[], other_resources=[
 (
  RT_MANIFEST, 1, manifest_template % dict(prog='py3o.ooservice'))], dest_base='py3o.ooservice', cmdline_style='pywin32')
py3o_openofficesetup = Target(description='Open Office headless as a windows service', script='service-setup.py', create_exe=True, create_dll=True, icon_resources=[], other_resources=[
 (
  RT_MANIFEST, 1, manifest_template % dict(prog='py3o.ooservice.setup'))], dest_base='py3o.ooservice.setup')
add_data = []
setup(options={'py2exe': {'compressed': 1, 
              'optimize': 2, 
              'packages': include_packages, 
              'includes': include_modules, 
              'excludes': excludes, 
              'dll_excludes': dll_excludes, 
              'dist_dir': dist_dir}}, zipfile='data\\shared.lib', console=[
 py3o_openofficesetup], windows=[], service=[
 py3o_openofficeservice], data_files=add_data, cmdclass=dict(nsi=NSI))