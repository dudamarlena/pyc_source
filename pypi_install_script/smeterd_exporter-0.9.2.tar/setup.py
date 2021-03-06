#!/usr/bin/env python
import re
import io
import codecs

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


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
    name = 'smeterd_exporter',
    description = 'A prometheus exporter for you smart meter.',
    version = '0.9.2',
    author = 'Nico Di Rocco',
    author_email = 'dirocco.nico@gmail.com',
    url = 'https://github.com/nrocco/smeterd_exporter',
    license = 'GPLv3',
    long_description = codecs.open('README.rst', 'rb', 'utf-8').read(),
    test_suite = 'nose.collector',
    download_url = 'https://github.com/nrocco/smeterd_exporter',
    include_package_data = True,
    install_requires = [
        'prometheus-client==0.0.19',
        'smeterd==2.7.2',
    ],
    tests_require = [
        'nose',
        'mock',
        'coverage',
    ],
    entry_points = {
        'console_scripts': [
            'smeterd_exporter = smeterd_exporter:main',
        ]
    },
    packages = find_packages(),
    zip_safe = False,
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    cmdclass = {
        'test': NoseTestCommand
    }
)
