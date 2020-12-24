#!/usr/bin/python

from setuptools import setup

setup(name='izaber_flask',
      version='1.20180813',
      description='Base load point for iZaber flask',
      url = 'https://github.com/zabertech/izaber-flask',
      download_url = 'https://github.com/zabertech/izaber-flask/archive/1.20180813.tar.gz',
      author='Aki Mimoto',
      author_email='aki+izaber@zaber.com',
      license='MIT',
      packages=['izaber_flask'],
      scripts=[],
      install_requires=[
          'izaber',
          'flask',
      ],
      dependency_links=[],
      zip_safe=False)

