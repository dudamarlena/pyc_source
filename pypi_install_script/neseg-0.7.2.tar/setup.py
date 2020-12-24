# -*- coding:utf-8 -*-
# Author：pastoral
# Date: 2020-01-11 20:54
from os.path import abspath, join, dirname
import sys
from setuptools import find_packages, setup

this_dir = abspath(dirname(__file__))
if sys.version_info[0] < 3:  # In Python3 TypeError: a bytes-like object is required, not 'str'
    long_description = '机构名称分割'
else:
    with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
        long_description = file.read()

setup(
    name="neseg", 
    version="0.7.2", 
    description="Named Entity Segmentation", 
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/myosmatrix/neseg',
    author='pastoral',
    author_email='huhongjun@gmail.com',
    license='Apache License 2.0',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: Chinese (Traditional)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Text Processing :: Linguistic'
    ],
    keywords='corpus,NLP',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    install_requires=['pyahocorasick==1.1.8','xlrd==1.1.0'],
        entry_points={
        'console_scripts': [
            'neseg=neseg.main:main',
        ],
    },       
)