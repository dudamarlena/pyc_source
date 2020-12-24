# -*- coding:utf-8 -*-
import win_unicode_console
from setuptools import setup
from setuptools import find_packages
win_unicode_console.enable()
long_description = open('README.md', 'r', encoding='utf-8').read()

setup(name='skBox',
      version='0.26.2',
      description='super kit box',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Hanmi Cheng',
      author_email='jxmt089659g@163.com',
      url='',
      packages=find_packages(),
      install_requires=["python-docx",
                        "numpy >= 1.14.0",
                        "pandas >= 0.22.0"],
      clssifiers=["Intended Audience :: Hanmi.cheng",
                  "Operating System :: OS Independent",
                  "Topic :: Text Processing :: Indexing",
                  "Programming Language :: Python :: 3.5",
                  ]
       )