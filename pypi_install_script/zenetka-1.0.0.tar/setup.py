
import os
import re
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


def _get_version():
    filename = os.path.join(os.path.dirname(__file__), 'zenetka', 'CHANGELOG.md')
    with open(filename, 'rt') as fd:
        pat = r"""
            (?P<version>\d+\.\d+)         # minimum 'N.N'
            (?P<extraversion>(?:\.\d+)*)  # any number of extra '.N' segments
            (?:
                (?P<prerel>[abc]|rc)      # 'a' = alpha, 'b' = beta
                                          # 'c' or 'rc' = release candidate
                (?P<prerelversion>\d+(?:\.\d+)*)
            )?
            (?P<postdev>(\.post(?P<post>\d+))?(\.dev(?P<dev>\d+))?)?
        """
        for line in fd:
            match = re.search(pat, line, re.VERBOSE)
            if match:
                return match.group()
    raise ValueError("Can't get version")


__version__ = _get_version()


class PyTest(TestCommand):
    user_options = [
        ('pytest-args=', 'a', "Arguments to pass to py.test"),
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def run_tests(self):
        import pytest
        import shlex
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


description = "Structured formatter for Python's logging"

try:
    if sys.version_info >= (3,):
        long_description = open('README.rst', 'rb').read().decode('utf-8')
    else:
        long_description = open('README.rst', 'r').read().decode('utf-8')
except IOError:
        long_description = description

setup(
    name='zenetka',
    version=__version__,
    author='Seznam.cz, a.s.',
    author_email='doporucovani-vyvoj@firma.seznam.cz',
    description=description,
    long_description=long_description,
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'ujson',
    ],
    tests_require=[
        'pytest',
    ],
    test_suite='tests',
    cmdclass={
        'test': PyTest,
    },
)
