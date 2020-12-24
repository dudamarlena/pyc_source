#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup
from setuptools.command.test import test as TestCommand


def read_md(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as mfile:
        string = mfile.read()
        return string


# Inspired by the example at https://pytest.org/latest/goodpractises.html


class NoseTestCommand(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Run nose ensuring that argv simulates running nosetests directly
        import nose
        nose.run_exit(argv=['nosetests'])


setup(
    name='kense',
    description='Selenium helpers for dealing with Kendo UI widgets',
    long_description=read_md('README.rst'),
    author='Jorge Javier Araya Navarro',
    author_email='jorge@esavara.cr',
    url='https://gitlab.com/esavara/kense',
    packages=['kense'],
    license="MIT",
    cmdclass={'test': NoseTestCommand},
    tests_require=["nose", "coverage"],
    install_requires=['selenium'],
    version_format='v{tag}.dev{commitcount}',
    setup_requires=['setuptools-git-version'],
)
