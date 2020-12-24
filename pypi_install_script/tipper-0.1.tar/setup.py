#!/usr/bin/env python

import os
import sys
from distutils.core import setup

def long_description():
    try:
        return open(os.path.join(sys.path[0], 'README.txt')).read()
    except Exception:
        return """
Tipper is a small utility for dumping `stack tracebacks`_ of running
Python processes.

Included is a module that, when imported, installs a `signal handler`_
for `SIGUSR1`_. Running ``kill -SIGUSR1 [pid]`` will cause the process
to dump the current stack trace of each thread to
``$TMPDIR/tipper-[unix timestamp]-[parent pid]-[pid].log``.

Tipper can also be used as `Django`_ application, though it has no
dependencies on Django itself.

Python 2.5 or newer is required. Python 3.x is also supported.

.. _stack tracebacks: http://docs.python.org/library/traceback.html
.. _signal handler: http://docs.python.org/library/signal.html
.. _SIGUSR1: http://en.wikipedia.org/wiki/SIGUSR1_and_SIGUSR2
.. _Django: http://www.djangoproject.com/
"""

setup(
    author='Brodie Rao',
    author_email='brodie@bitheap.org',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: No Input/Output (Daemon)',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Utilities',
    ],
    description='A utility for dumping stack traces of running Python processes',
    download_url='http://bitheap.org/tipper/tipper-0.1.tar.gz',
    keywords='daemon debugging django process server traceback',
    license='MIT',
    long_description=long_description(),
    name='tipper',
    packages=['tipper'],
    url='http://bitheap.org/tipper/',
    version='0.1',
)
