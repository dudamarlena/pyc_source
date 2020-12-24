#!/usr/bin/env python
from glob import glob
from distutils.core import setup
import os

import higgins


scripts = ['bin/hn']
if os.name == 'nt':
    scripts.append('bin/hn.bat')

setup(name='Higgins',
      version=higgins.__version__,
      description='Higgins',
      author='Bertrand Chenal',
      author_email='bertrand@adimian.com',
      url='https://bitbucket.org/adimian/higgins',
      license='MIT',
      scripts=scripts,
      packages=['higgins'],
      install_requires = [
          'sqlalchemy',
          'flask',
          'pyyaml'
      ],
      package_data = {
          'higgins': [
              'template/*html',
              'static/css/*',
              'static/fonts/*',
              'static/js/*',
          ],
    },
  )
