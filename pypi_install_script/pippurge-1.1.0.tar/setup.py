#!/usr/bin/env python
# coding: utf8

from setuptools import setup

with open('README.rst', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='pippurge',
    version='1.1.0',
    keywords=['pip', 'dependency', 'purge', 'pip-purge', 'pipurge'],
    description='Enhancement for pip uninstall command, that it removes all dependencies of an uninstalled package.',
    long_description=readme,
    author='zhoujin7',
    author_email='zhoujin7@foxmail.com',
    url='https://github.com/zhoujin7/pippurge',
    py_modules=['pippurge'],
    license='Apache License 2.0',
    zip_safe=False,
    entry_points={
        'console_scripts': ['pippurge = pippurge:main']
    },
    classifiers=[
        'Environment :: Console',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent'
    ]
)
