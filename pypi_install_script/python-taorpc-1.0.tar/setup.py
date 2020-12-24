#!/usr/bin/env python

from distutils.core import setup

setup(
    name='python-taorpc',
    version='1.0',
    description='Enhanced version of python-bitcoinrpc for use with Tao',
    long_description=open('README.rst').read(),
    author='Bryce Weiner',
    author_email='<bryce@tao.network>',
    maintainer='Bryce Weiner',
    maintainer_email='<bryce@tao.network>',
    url='http://www.github.com/taoblockchain/python-taorpc',
    packages=['taorpc'],
    classifiers=[
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)', 'Operating System :: OS Independent'
    ]
)
