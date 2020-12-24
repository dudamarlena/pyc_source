# -*- coding: utf-8 -*-
from __future__ import with_statement
from setuptools import setup


def get_version(fname='flint/__init__.py'):
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


def get_long_description():
    descr = []
    for fname in 'README.rst', 'CHANGES.txt':
        with open(fname) as f:
            descr.append(f.read())
    return '\n\n'.join(descr)


setup(
    name='flint',
    version=get_version(),
    description="the modular Python source code checker",
    long_description=get_long_description(),
    keywords='flint pep8 pyflakes flake8 lint',
    author='Florent Xicluna',
    author_email='florent.xicluna@gmail.com',
    url='https://github.com/flintwork/flint',
    license='Expat license',
    packages=['flint'],
    zip_safe=False,
    install_requires=[
        'setuptools',
        'pep8 >= 1.4.3',
        'pyflakes >= 0.6.1',
    ],
    entry_points={
        'console_scripts': [
            'flint = flint:main',
        ],
        'flint.extension': [
            'F = flint._pyflakes:FlakesChecker',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ],
)
