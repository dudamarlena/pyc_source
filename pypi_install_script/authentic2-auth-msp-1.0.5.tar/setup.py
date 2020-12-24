#!/usr/bin/python
import sys
import os

from setuptools import setup, find_packages
from setuptools.command.install_lib import install_lib as _install_lib
from distutils.command.build import build as _build
from distutils.command.sdist import sdist
from distutils.cmd import Command

class compile_translations(Command):
    description = 'compile message catalogs to MO files via django compilemessages'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            from django.core.management.commands.compilemessages import \
                    compile_messages
            for path, dirs, files in os.walk('src'):
                if 'locale' not in dirs:
                    continue
                curdir = os.getcwd()
                os.chdir(os.path.realpath(path))
                compile_messages(sys.stderr)
                os.chdir(curdir)
        except ImportError:
            print
            sys.stderr.write('!!! Please install Django >= 1.4 to build translations')
            print
            print


class build(_build):
    sub_commands = [('compile_translations', None)] + _build.sub_commands

class build(_build):
    sub_commands = [('compile_translations', None)] + _build.sub_commands

class eo_sdist(sdist):

    def run(self):
        print "creating VERSION file"
        if os.path.exists('VERSION'):
            os.remove('VERSION')
        version = get_version()
        version_file = open('VERSION', 'w')
        version_file.write(version)
        version_file.close()
        sdist.run(self)
        print "removing VERSION file"
        if os.path.exists('VERSION'):
            os.remove('VERSION')

class install_lib(_install_lib):
    def run(self):
        self.run_command('compile_translations')
        _install_lib.run(self)

def get_version():
    import glob
    import re
    import os

    version = None
    for d in glob.glob('src/*'):
        if not os.path.isdir(d):
            continue
        module_file = os.path.join(d, '__init__.py')
        if not os.path.exists(module_file):
            continue
        for v in re.findall("""__version__ *= *['"](.*)['"]""",
                open(module_file).read()):
            assert version is None
            version = v
        if version:
            break
    assert version is not None
    if os.path.exists('.git'):
        import subprocess
        p = subprocess.Popen(['git','describe','--dirty','--match=v*'],
                stdout=subprocess.PIPE)
        result = p.communicate()[0]
        assert p.returncode == 0, 'git returned non-zero'
        new_version = result.split()[0][1:]
        assert new_version.split('-')[0] == version, '__version__ must match the last git annotated tag'
        version = new_version.replace('-', '.')
    return version

README = file(os.path.join(
    os.path.dirname(__file__),
    'README')).read()

setup(name='authentic2-auth-msp',
        version=get_version(),
        license='AGPLv3',
        description='Authentic2 mon.service-public.fr plugin',
        long_description=README,
        author="Entr'ouvert",
        url='https://repos.entrouvert.org/authentic2-auth-msp.git',
        author_email="info@entrouvert.com",
        packages=find_packages('src'),
        package_dir={
            '': 'src',
        },
        package_data={
            'authentic2_auth_msp': [
                  'templates/authentic2_auth_msp/*.html',
                  'static/authentic2_auth_msp/js/*.js',
                  'static/authentic2_auth_msp/css/*.css',
                  'static/authentic2_auth_msp/img/*.png',
                  'static/authentic2_auth_msp/img/*.jpg',
                  'static/authentic2_auth_msp/img/*.gif',
                  'static/authentic2_auth_msp/img/bg/*.png',
                  'static/authentic2_auth_msp/img/bg/*.jpg',
                  'static/authentic2_auth_msp/img/bg/*.gif',
                  'locale/fr/LC_MESSAGES/django.po',
                  'locale/fr/LC_MESSAGES/django.mo',
            ],
        },
        install_requires=[
            'authentic2',
            'requests',
            'requests-oauthlib',
            'django-sekizai',
        ],
        entry_points={
            'authentic2.plugin': [
                'authentic2-auth-msp = authentic2_auth_msp:Plugin',
            ],
        },
        cmdclass={
            'build': build,
            'install_lib': install_lib,
            'compile_translations': compile_translations,
            'sdist': eo_sdist},

)
