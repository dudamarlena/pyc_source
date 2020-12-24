#!/usr/bin/env python
# coding=utf-8
from setuptools import setup

setup(name='znz_spider',
      version='0.1.0',
      description='我还能说什么呢？',
      url='https://github.com/zhangnaizhao/znz_spider.git',
      author='zhangnaizhao',
      author_email='zhang_naizhao@163.com',
      license='MIT',
      packages=['spider_tool', 'data_processing'],
      install_requires=[
          'numpy',
          'pandas',
          'scikit-learn',
          'requests',
          'lxml'
      ],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ]
      )
