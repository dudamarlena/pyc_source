# -*- coding: utf-8 -*-
"""
AMPL Remote Driver
------------------

AMPL Remote Driver is a solver driver for AMPL based on a REST API that
allows solving models on a remote machine while using AMPL on a local machine.

Links
`````

* GitHub Repository: https://github.com/ampl/ampl-remote
* PyPI Repository: https://pypi.python.org/pypi/amplremote
"""
from setuptools import setup
import os


def ls_dir(base_dir):
    """List files recursively."""
    return [
        os.path.join(dirpath.replace(base_dir, '', 1), f)
        for (dirpath, dirnames, files) in os.walk(base_dir)
        for f in files
    ]

setup(
    name='amplremote',
    version='v0.1.0',
    description='AMPL Remote Driver',
    long_description=__doc__,
    license='BSD-3',
    platforms='any',
    author='Filipe Brandão',
    author_email='fdabrandao@ampl.com',
    url='http://ampl.com/',
    download_url='https://github.com/ampl/amplpy',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    install_requires=open('requirements.txt').read().split('\n'),
    packages=['amplremote'],
    scripts=[
      'scripts/remote', 'scripts/remote.bat',
      'scripts/amplserver', 'scripts/amplserver.bat'],
    package_data={'': ls_dir('amplremote/')},
)
