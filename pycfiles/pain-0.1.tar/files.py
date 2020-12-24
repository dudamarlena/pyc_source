# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jack/code/pain/pain/files.py
# Compiled at: 2013-04-29 05:39:52
import string

class File(object):

    def __init__(self, name):
        self.name = name
        self.content = ''

    def template(self, values):
        return string.Template(self.content).safe_substitute(**values)


class SetupPy(File):

    def __init__(self):
        super(SetupPy, self).__init__('setup.py')
        self.content = "\n\t\t\tfrom setuptools import setup, find_packages\n\t\t\t\n\t\t\tsetup(\n\t\t\t\tname='$name',\n\t\t\t\tversion='0.1',\n\t\t\t\tdescription='$description',\n\t\t\t\tclassifiers=[],\n\t\t\t\tkeywords='',\n\t\t\t\tauthor='$author',\n\t\t\t\tauthor_email='$author_email',\n\t\t\t\turl='$url',\n\t\t\t\tlicense='$license',\n\t\t\t\tpackages=find_packages(),\n\t\t\t\tinclude_package_data=True,\n\t\t\t\ttest_suite='nose.collector',\n\t\t\t\tzip_safe=False,\n\t\t\t)\n\t\t"


class SetupCfg(File):

    def __init__(self):
        super(SetupCfg, self).__init__('setup.cfg')
        self.content = ''


class Requirements(File):

    def __init__(self):
        super(Requirements, self).__init__('requirements.txt')
        self.content = ''


class TODO(File):

    def __init__(self):
        super(TODO, self).__init__('TODO.md')
        self.content = ''


class README(File):

    def __init__(self):
        super(README, self).__init__('README.md')
        self.content = ''


class MANIFEST(File):

    def __init__(self):
        super(MANIFEST, self).__init__('MANIFEST.in')
        self.content = ''


class TravisYaml(File):

    def __init__(self):
        super(TravisYaml, self).__init__('.travis-yml')
        self.content = ''


class GitIgnore(File):

    def __init__(self):
        super(GitIgnore, self).__init__('.gitignore')
        self.content = '\n\t\t\t*.py[cod]\n\t\t\t.env\n\t\t\t# C extensions\n\t\t\t*.so\n\n\t\t\t# Packages\n\t\t\t*.egg\n\t\t\t*.egg-info\n\t\t\tdist\n\t\t\tbuild\n\t\t\teggs\n\t\t\tparts\n\t\t\tbin\n\t\t\tvar\n\t\t\tsdist\n\t\t\tdevelop-eggs\n\t\t\t.installed.cfg\n\t\t\tlib\n\t\t\tlib64\n\n\t\t\t# Installer logs\n\t\t\tpip-log.txt\n\n\t\t\t# Unit test / coverage reports\n\t\t\t.coverage\n\t\t\t.tox\n\t\t\tnosetests.xml\n\n\t\t\t# Translations\n\t\t\t*.mo\n\n\t\t\t# Mr Developer\n\t\t\t.mr.developer.cfg\n\t\t\t.project\n\t\t\t.pydevproject\n\t\t'


class Env(File):

    def __init__(self):
        super(Env, self).__init__('.env')
        self.content = '\n\t\t\tuse_env $name\n\t\t'


class Init(File):

    def __init__(self):
        super(Init, self).__init__('__init__.py')
        self.content = ''