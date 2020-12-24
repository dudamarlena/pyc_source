# vim:fileencoding=utf-8
"""
Packaging bits!
"""
from __future__ import print_function

import ast

from setuptools import setup, find_packages


def get_version():
    """
    Get the version from the source, but without importing.
    """
    with open('sj.py') as source:
        for node in ast.walk(ast.parse(source.read(), 'sj.py')):
            if node.__class__.__name__ == 'Assign' and \
               node.targets[0].__class__.__name__ == 'Name' and \
               node.targets[0].id == '__version__':
                return node.value.s


def get_long_description():
    """
    Use the ``README.rst`` as the long description.
    """
    with open('README.rst') as readme:
        return readme.read().strip()


setup(
    name='sj',
    author='Dan Buch',
    author_email='dan@meatballhat.com',
    license='MIT',
    keywords='snakey json',
    url='https://github.com/hamfist/sj',
    description='Enforcer of snakey JSON',
    long_description=get_long_description(),
    version=get_version(),
    packages=find_packages(),
    py_modules=['sj'],
    platforms=['any'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: SunOS/Solaris',
        'Programming Language :: Python :: 2.7',
        # FIXME: ijson is currently hosed on Python 3
        # 'Programming Language :: Python :: 3.3',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    install_requires=[
        'ijson == 1.1'
    ],
    entry_points={
        'console_scripts': [
            'sj = sj:main'
        ]
    }
)
