#!/usr/bin/env python
"""
 Copyright (C) 2016 by SolarWinds, LLC.
 All rights reserved.
"""

import distutils.ccompiler
from setuptools import setup, Extension

version = '1.5.11'

# conditionally build extensions if liboboe and liboboe-dev are available on this platform
# otherwise, will function in no-op mode: no tracing, but all API endpoints available
compiler = distutils.ccompiler.new_compiler()
if compiler.has_function('oboe_metadata_init', libraries=('oboe',)):
    oboe_module = Extension('oboe._oboe_ext',
                            sources=['oboe/oboe_wrap.cxx'],
                            depends=['oboe/oboe.hpp'],
                            libraries=['oboe'])
    ext_modules = [oboe_module]
else:
    ext_modules = []

setup(name = 'oboe',
      version = version,
      author = 'SolarWinds, LLC',
      author_email = 'traceviewsupport@solarwinds.com',
      url = 'https://traceview.solarwinds.com/TraceView/Python',
      download_url = 'https://pypi.python.org/pypi/oboe',
      description  = 'TraceView Oboe libraries, instrumentation, and web middleware components '
      'for WSGI, Django, and Tornado.',
      long_description = open('README.md').read(),
      keywords='traceview tracelytics oboe liboboe instrumentation performance wsgi middleware django',
      ext_modules = ext_modules,
      packages = ['oboe', 'oboeware'],
      license = 'LICENSE.txt',
      install_requires = ['decorator'],
      )
