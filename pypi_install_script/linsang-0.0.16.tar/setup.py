import re
import sys
from os.path import dirname, abspath, join
from setuptools import setup

from setuptools.command.test import test as TestCommand

HERE = dirname(abspath(__file__))
VERSION = re.findall(\
                r'python-linsang \(([a-zA-Z0-9\.\+~-]+)\)',\
                open(join(HERE, 'debian', 'changelog'), 'rt').readline())[0]
VERSION = VERSION.replace('~dev', 'a').replace('~rc', 'rc').replace('+', '.post')

class PyTest(TestCommand):

    user_options = [
        ('pytest-args=', 'a', "Arguments to pass to py.test"),
    ]

    def run(self):
        TestCommand.run(self)

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(
    name="linsang",
    version=VERSION,
    author='Seznam.cz, a.s.',
    author_email="doporucovani@firma.seznam.cz",
    description=(
        "Poskytuje handler pro logování do souboru z více procesů."
    ),
    license="commercial",
    url='http://cml.kancelar.seznam.cz/doporucovani',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Logging',
    ],
    packages=['linsang'],
    install_requires=[
        'posix_ipc',
    ],
    tests_require=[
        'mock',
        'mypy==0.521',
        'pylint<2',
        'pytest>=2.6',
    ],
    test_suite='tests',
    cmdclass={
        'test': PyTest
    },
)
