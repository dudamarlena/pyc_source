#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'Dalwar Hossain'
__email__ = 'dalwar.hossain@protonmail.com'


from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='pyrainbowterm',
      version='1.0',
      description='pyrainbowterm - Smart custom print function with color and log information support',
      long_description=readme(),
      classifiers=[
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='terminal colors xterm python colored output',
      url='https://github.com/dharif23/pyrainbowterm',
      author='Dalwar Hossain',
      author_email='dalwar.hossain@protonmail.com',
      license='MIT',
      packages=['pyrainbowterm'],
      include_package_data=True,
      zip_safe=False)