#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
setup(name='peer2peer',
      version='2.1.0',
      description='peer 2 peer',
      py_modules=['peer2peer'],
      scripts=['peer2peer.py'],
      license='MIT',
      platforms='any',
      install_requires=[
          'websocket-client',
          'gevent-websocket',
          'gevent','future','docopt'
          ],
)
