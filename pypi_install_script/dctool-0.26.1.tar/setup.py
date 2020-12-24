# -*- coding:utf-8 -*-
import win_unicode_console
from setuptools import setup
from setuptools import find_packages
win_unicode_console.enable()
long_description = open('README.md', 'r', encoding='utf-8').read()

setup(name='dctool',
      version='0.26.1',
      description='Tool module used within datacenter',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Hanmi Cheng',
      author_email='hanmi.cheng@xinjifamily.com',
      url='',
      packages=find_packages(),
      install_requires=["python-docx",
                        "numpy >= 1.14.0",
                        "pandas >= 0.22.0",
                        "scikit-learn == 0.19.2",
                        "baidu-aip",
                        "pyhdfs >= 0.2.2",
                        "pycrypto >= 2.6.1",
                        "pycryptodome >= 3.8.2",
                        "jieba2 >= 0.13"],
      clssifiers=["Intended Audience :: Hanmi.cheng",
                  "Operating System :: OS Independent",
                  "Topic :: Text Processing :: Indexing",
                  "Programming Language :: Python :: 3.5",
                  ]
       )