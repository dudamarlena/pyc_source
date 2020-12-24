#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
from codecs import open
from os import path
from distutils.command.install_data import install_data
from distutils.core import setup, Extension
from setuptools.command.install_lib import install_lib
from setuptools.command.install_scripts import install_scripts
from setuptools.command.build_ext import build_ext

here = path.abspath(path.dirname(__file__))

class omniidlExtension(Extension, object):
    def __init__(self, name, sources=[]):
        super(omniidlExtension, self).__init__(name = name, sources = sources)


class InstallomniidlLibsData(install_data):
    def run(self):
        print("InstallomniidlLibsData")

class InstallomniidlLibs(install_lib):
    def run(self):
        print("InstallomniidlLibs")

class InstallomniidlScripts(install_scripts):
    def run(self):
        print("InstallomniidlScripts")

class BuildomniidlExt(build_ext):
    def run(self):
        print("BuildomniidlExt")


setup(
    name='piptest_0922',
    version='1.0.2',
    description='Dummy',
    long_description="description",
    url='https://github.com/Nobu19800/piptest',
    author='nobu',
    author_email='nobu@nobu777.net',
    license='MIT',
    install_requires=[],
    keywords='dummy',
    packages=find_packages(exclude=('tests')),
    entry_points={
        "console_scripts": [
            "piptest=piptest.__init__:main",
        ],
    },
    cmdclass={
        'build_ext': BuildomniidlExt,
        'install_data': InstallomniidlLibsData,
        'install_lib': InstallomniidlLibs,
        'install_scripts': InstallomniidlScripts
    },
    ext_modules=[omniidlExtension(name="example_extension", sources=["test.idl"])],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
    ],
)