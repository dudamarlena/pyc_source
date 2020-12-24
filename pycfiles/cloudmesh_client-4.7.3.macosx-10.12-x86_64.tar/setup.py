# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/setup.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
import os, sys, yaml
from setuptools.command.install import install
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.util import banner
make = '\n    test:\n    - echo "hallo world"\n    github:\n    - git commit -a\n    - git push\n    clean:\n    - rm -rf *.egg-info *.eggs\n    - rm -rf docs/build\n    - rm -rf build\n    - rm -rf dist\n    doc:\n    - sphinx-apidoc -o docs/source cloudmesh_client\n    - cd docs; make -f Makefile html\n    view:\n    - open docs/build/html/index.html\n    pypi:\n    - python setup.py install\n    - python setup.py sdist bdist_wheel\n    - python setup.py bdist_wheel upload -r {repo}\n    - python setup.py sdist upload -r {repo}\n    register:\n    - python setup.py register -r {repo}\n    tag:\n    - bin/new_version.sh\n    rmtag:\n    - git tag\n    - echo "rm Tag?"; read TAG; git tag -d $$TAG; git push origin :refs/tags/$$TAG\n    install:\n    - python setup.py install\n'
clean_python = '\n    find . -name "*~" -exec rm \\{\\} \\;\n    find . -name "*.pyc" -exec rm \\{\\} \\;\n'

def parse_requirements(filename):
    """
    load the requirement form the specified file
    :param filename: the filename
    :return:
    """
    lineiter = (line.strip() for line in open(filename))
    return [ line for line in lineiter if line and not line.startswith('#') ]


def os_execute(commands):
    for command in commands.split('\n'):
        command = command.strip()
        print(command)
        os.system(command)


def get_version_from_git():
    r = Shell.git('tag').split('\n')[(-1)]
    return r


def check_pip():
    """
    major = int(pip.__version__.split(".")[0])
    if major < 7:
        print("")
        print("    ERROR: Pip version", pip.__version__, "is to old.")
        print("    Tip:   Please update pip with ")
        print("")
        print("             pip install pip -U")
        print("")
        sys.exit()
    """
    pass


def makefile(tag, **kwargs):
    script = ('\n').join(yaml.load(make)[tag])
    commands = ('\n').join(yaml.load(make)[tag]).format(**kwargs)
    banner('RUNNING')
    os_execute(commands)


def Make(action, **kwargs):

    class InstallAction(install):

        def run(self):
            makefile(action, **kwargs)
            if action == 'clean':
                os.system(clean_python)

    return InstallAction