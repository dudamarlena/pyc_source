"""
setup.py

Setup and configuration script for the package.

:author:        Kyberdin (Stephen Stauts)
:created:       13/02/2020   (DD/MM/YYYY)
:copyright:     See package or project LICENSE file
"""

# Standard Packages
from setuptools import setup, find_packages

# Dependency Packages

# Module (local) Packages


MODULE_NAME = 'findep'          # This is the name as seen by scripts
PACKAGE_NAME = MODULE_NAME      # This is the name as seen by PyPI

# https://github.com/paramiko/paramiko/blob/master/setup.py#L38
_pkg_attrs = {}
with open('src/{}/version.py'.format(MODULE_NAME)) as f:
    exec(f.read(), None, _pkg_attrs)


setup(
    name=PACKAGE_NAME,
    version=_pkg_attrs['__version__'],
    description='Find dependency files.',
    long_description='',
    url='https://gitlab.com/kyberdin/findep',
    author='Kyberdin',
    author_email='kyberdin.git@gmail.com',
    license='MIT',
    keywords='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: System :: Logging'
    ],
    package_dir={'':'src'},
    packages=find_packages(
        where='src',
        exclude=[],
    ),
    python_requires='>=3.5',
    install_requires=[
        'cachetools>=4.0.0',
        'docopt>=0.6.2',
    ],
)
