#!/usr/bin/env python
# -*- coding:utf-8 -*-
from setuptools import setup

setup(name='dadan',
      version='0.2.2',
      description='dadan Natural Language Processing',
      author='dadan',
      author_email='dadan@qq.com',
      license='MIT',
      packages=['dadan'],
      package_dir={'dadan': 'dadan'},
      package_data={'dadan': ['*.*', 'cluster/*', 'data/*', 'model/*',
		'normal/*', 'segment/*', 'segment/dict/*','segment/model/*',
		'sentiment/*', 'sentiment/model/*', 'topic/*']}
      )
