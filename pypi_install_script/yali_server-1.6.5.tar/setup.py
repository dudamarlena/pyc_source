# coding:utf-8
#!/usr/bin/env python
#!/usr/bin/env python3

import codecs
import os
import sys
try:
    from setuptools import setup
except:
    from distutils.core import setup

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

NAME = "yali_server"
PACKAGES = ['start_server','cgi-bin']
DESCRIPTION = "this is for log record for ios or android"
LONG_DESCRIPTION = "this is for log record for ios or android,有问题可以联系我，温亚莉"
KEYWORDS = "keyword"
AUTHOR = "wenyali"
AUTHOR_EMAIL = "2917073217@qq.com"
URL = "https://github.com/wenyali/yali_server.git"
VERSION = "1.6.5"
LICENSE = "MIT"
setup(
      name =NAME,version = VERSION,
      description = DESCRIPTION,long_description =LONG_DESCRIPTION,
      classifiers =[
                    'License :: OSI Approved :: MIT License',
                    'Programming Language :: Python',
                    'Intended Audience :: Developers',
                    'Operating System :: OS Independent',
                    ],
      keywords =KEYWORDS,author = AUTHOR,
      author_email = AUTHOR_EMAIL,url = URL,
      packages = PACKAGES,include_package_data=True,zip_safe=True,
      entry_points={
      "console_scripts": [
                          "yali_server = start_server.start_server:index",
                          ]
      },
      
      )
