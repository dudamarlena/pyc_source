from distutils.core import setup
from distutils.extension import Extension

setup(
name = 'recordb',
packages = ['recordb'], # this must be the same as the name above
version = '1.3',
description = 'A fast and easy-to-use embedded database for python',
license='MIT',
author = 'Brian Gikonyo',
author_email = 'colasgikonyo@gmail.com',
url = 'https://bitbucket.org/GikonyoBrian/recordb', 
download_url = 'https://bitbucket.org/GikonyoBrian/recordb/get/recordb.tar.gz',
keywords = ['databases', 'embedded databases', 'local database', 'fast', 'easy-to-use', 'python2', 'python'],
install_requires=[
          'ujson',
      ],
ext_modules = [Extension("recordb.recordb", ["recordb/recordb.c"])],
classifiers = [
	'Development Status :: 3 - Alpha',
 	'Environment :: Console',
 	'Intended Audience :: Developers',
 	'Programming Language :: Python',
 	'Programming Language :: Python :: 2',
 	'Programming Language :: Python :: 2.6',
 	'Programming Language :: Python :: 2.7',],
)
