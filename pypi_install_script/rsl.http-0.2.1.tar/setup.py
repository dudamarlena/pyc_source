#!/usr/bin/env python
##############################################################################
# Copyright 2008-2009, Gerhard Weis
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#  * Neither the name of the authors nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT
##############################################################################
import os
from setuptools import setup
from setuptools import find_packages
# for setuptools see: http://peak.telecommunity.com/DevCenter/setuptools

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name = 'rsl.http',
      version = '0.2.1',
      package_dir={'': 'src'},
      packages = find_packages('src', exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      include_package_data = True,
      
      namespace_packages = ['rsl'],
      
      # dependencies:
      install_requires = ['rsl >= 0.2.1',
                          'rsl.xsd >= 0.2.2',
                          'rsl.wsdl1 >= 0.2.2',
                          'lxml >= 2.0',
                          'zope.interface',
                          'setuptools'],
      
      # PyPI metadata
      author='Gerhard Weis',
      author_email='gerhard.weis@proclos.com',
      description='Remote Service Library http binding module',
      license = 'BSD',
      #keywords = '',
      url='http://rslib.sourceforge.net',

      long_description=read('README.txt') +
                       read('CHANGES.txt'),
      
      #download_url='',
      classifiers = ['Development Status :: 3 - Alpha',
                     'Environment :: Web Environment',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: BSD License',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python',
                     'Topic :: Internet',
                     'Topic :: Software Development :: Libraries :: Python Modules',
                     'Topic :: System :: Networking',
                     ],
      entry_points = {'rsl.register': ['method = rsl.http.factories:register'],
                      'rsl.wsdl1.service.port': [ 'http://schemas.xmlsoap.org/wsdl/http/ = rsl.http.wsdl1:httpportfactory' ],
                      'rsl.wsdl1.binding': [ 'http://schemas.xmlsoap.org/wsdl/http/ = rsl.http.wsdl1:httpbindingfactory' ],
                      'rsl.wsdl1.binding.operation' : [ 'http://schemas.xmlsoap.org/wsdl/http/ = rsl.http.wsdl1:httpoperationfactory' ],
                      'rsl.wsdl1.binding.operation.input' : [ 'http://schemas.xmlsoap.org/wsdl/http/ = rsl.http.wsdl1:httpparaminfofactory' ],
                      'rsl.wsdl1.binding.operation.output' : [ 'http://schemas.xmlsoap.org/wsdl/http/ = rsl.http.wsdl1:httpparaminfofactory' ] }
     )
