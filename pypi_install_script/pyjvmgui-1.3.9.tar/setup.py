import errno
import os
from os import path
from sys import path as sys_path

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install

this_directory = path.abspath(path.dirname(__file__))
srcdir = path.join(this_directory, "src/")
sys_path.insert(0, srcdir)

from pyjvm_util.globals import PYJVMGUI_HOME


def post_install():
    try:
        os.makedirs(PYJVMGUI_HOME)
        print "Created directory '{0}'".format(PYJVMGUI_HOME)
    except OSError as e:
        if e.errno != errno.EEXIST:
            pass


class DevelopWithRt(develop):
    def run(self):
        develop.run(self)
        post_install()


class InstallWithRt(install):
    def run(self):
        install.run(self)
        post_install()


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='pyjvmgui',
    version='1.3.9',
    url='https://github.com/MatevzFa/pyjvm',
    license='GPL-3.0',
    author='matevz',
    author_email='mf6422@student.uni-lj.si',
    description='A GUI for the PyJVM',

    long_description=long_description,
    long_description_content_type='text/markdown',

    packages=find_packages('src'),
    py_modules=['pyjvmgui'],

    data_files=[
        (PYJVMGUI_HOME, [
            os.path.join('src', 'pyjvm_gui', 'qml', 'App.qml'),
            os.path.join('src', 'pyjvm_gui', 'qml', 'Separator.qml')
        ])
    ],

    package_dir={'': 'src'},

    entry_points={
        'console_scripts': ['pyjvmgui=pyjvmgui:main']
    },

    install_requires=['PySide2'],

    cmdclass={
        'install': InstallWithRt,
        'develop': DevelopWithRt,
    },
)
