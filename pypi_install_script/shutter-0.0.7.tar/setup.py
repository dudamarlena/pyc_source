#!/usr/bin/env python
#encoding: utf-8

from setuptools import setup


setup(name='shutter',
      version='0.0.7',
      description='ctypes interface for libgphoto2',
      author='bitcraft',
      author_email='leif.theden@gmail.com',
      keywords=['gphoto', 'libgphoto2', 'capture', 'shutter'],
      packages=['shutter'],
      requires=['six'],
      license='GPLv3',
      long_description='https://github.com/bitcraft/shutter',
      classifiers=[
          'Intended Audience :: Developers',
          'Development Status :: 3 - Alpha',
          'Topic :: Multimedia :: Graphics :: Capture :: Digital Camera',
          'Programming Language :: Python :: 2.7',
      ],
)
