# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/javatools/cheetah/setuptools.py
# Compiled at: 2018-12-14 21:30:42
# Size of source mod 2**32: 5280 bytes
"""
Replacement setuptools/distutils build_py command which also
compiles Cheetah templates to Python

author: Christopher O'Brien  <obriencj@gmail.com>
license: LGPL v.3
"""
from distutils.core import Command
from distutils.util import newer
import distutils.command.build_py as build_py
from glob import glob
from os import makedirs
from os.path import basename, exists, join, splitext
DEFAULT_CONFIG = 'extras/cheetah.cfg'

class cheetah_cmd(Command):
    __doc__ = '\n    command that compiles Cheetah template files into Python\n    '


class cheetah_build_py_cmd(build_py):
    __doc__ = '\n    build_py command with some special handling for Cheetah template\n    files. Takes tmpl from package source directories and compiles\n    them for distribution. This allows me to write tmpl files in the\n    src dir of my project, and have them get compiled to py/pyc/pyo\n    files during the build process.\n    '

    def find_package_templates(self, package, package_dir):
        self.check_package(package, package_dir)
        template_files = glob(join(package_dir, '*.tmpl'))
        templates = []
        for f in template_files:
            template = splitext(basename(f))[0]
            templates.append((package, template, f))

        return templates

    def build_package_templates(self):
        for package in self.packages:
            package_dir = self.get_package_dir(package)
            templates = self.find_package_templates(package, package_dir)
            for package_, template, template_file in templates:
                assert package == package_
                self.build_template(template, template_file, package)

    def build_template(self, template, template_file, package):
        """
        Compile the cheetah template in src into a python file in build
        """
        try:
            import Cheetah.Compiler as Compiler
        except ImportError:
            self.announce('unable to import Cheetah.Compiler, build failed')
            raise
        else:
            comp = Compiler(file=template_file, moduleName=template)
        conf_fn = DEFAULT_CONFIG
        if exists(conf_fn):
            with open(conf_fn, 'rt') as (config):
                comp.updateSettingsFromConfigFileObj(config)
        comp.setShBang('')
        comp.addModuleHeader('pylint: disable=C,W,R,F')
        outfd = join(self.build_lib, *package.split('.'))
        outfn = join(outfd, template + '.py')
        if not exists(outfd):
            makedirs(outfd)
        if newer(template_file, outfn):
            self.announce('compiling %s -> %s' % (template_file, outfd), 2)
            with open(outfn, 'w') as (output):
                output.write(str(comp))

    def get_template_outputs(self, include_bytecode=1):
        built = list()
        for package in self.packages:
            package_dir = self.get_package_dir(package)
            templates = self.find_package_templates(package, package_dir)
            for _, template, _ in templates:
                outfd = join(self.build_lib, *package.split('.'))
                outfn = join(outfd, template + '.py')
                built.append(outfn)
                if include_bytecode:
                    if self.compile:
                        built.append(outfn + 'c')
                    if self.optimize > 0:
                        built.append(outfn + 'o')

        return built

    def get_outputs(self, include_bytecode=1):
        outputs = build_py.get_outputs(self, include_bytecode)
        outputs.extend(self.get_template_outputs(include_bytecode))
        return outputs

    def run(self):
        if self.packages:
            self.build_package_templates()
        build_py.run(self)