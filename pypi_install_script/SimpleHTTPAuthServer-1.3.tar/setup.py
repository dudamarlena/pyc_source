#!/usr/bin/env python

from SimpleHTTPAuthServer import __version__, __prog__
from distutils.core import setup

setup(
	name=__prog__,
	version=__version__,
	description='Simple HTTP and HTTPS Auth Server',
	author='Michael Li',
	author_email='me@tianhui.li',
	url='https://github.com/tianhuil/SimpleHTTPAuthServer/',
	packages=[__prog__],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
