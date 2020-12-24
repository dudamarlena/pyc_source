#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
setup(name='pkcrypt2',
      version='1.10.4',
      description='public key cryptography',
      long_description=open('README.md').read(),
      author='Joel Ward',
      author_email='jmward@gmail.com',
      license='MIT',
      platforms='any',
      url='https://gist.github.com/val314159/ae5c886a593fc1523d936baf690e8343',
      py_modules=['pkcrypt2','x85'],
      scripts=['pkcrypt2.py','x85.py'],
      install_requires=['fastecdsa','pyaml','cryptography'],
     )
