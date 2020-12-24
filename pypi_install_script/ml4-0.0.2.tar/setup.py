#!/usr/bin/env python

import re


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


version = '0.0.2'

if not version:
    raise RuntimeError('Cannot find version information')


with open('README.rst', 'rb') as f:
    readme = f.read().decode('utf-8')

setup(
    name='ml4',
	author='Jiao Shuai',
	author_email='jiaoshuaihit@gmail.com',
    version=version,
    description='TechYoung Machine Learning ToolKit',
    long_description=readme,
    packages=['ml4'],
    install_requires=['numpy'],
    include_package_data=True,
    url='http://ml4.techyoung.cn',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)
