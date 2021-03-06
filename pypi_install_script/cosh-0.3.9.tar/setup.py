# -*- coding: utf-8 -*-

import os
import subprocess

from setuptools import setup, find_packages

# Fetch version from git tags, and write to version.py.
# Also, when git is not available (PyPi package), use stored version.py.
version_py = os.path.join(os.path.dirname(__file__), 'version.py')

try:
  p = subprocess.Popen(['git', 'describe', '--tags'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  o = p.communicate()
  if p.returncode != 0:
    raise Exception('git describe failed to execute reason: %s' % o[1])
  version_git = o[0].rstrip().decode('utf-8')
except Exception:
  version_git = '0.1.0'

version_msg = "# Do not edit this file"
with open(version_py, 'w') as fh:
  fh.write('%s%s__version__=%s' % (version_msg, os.linesep, version_git))

version = '{ver}'.format(ver=version_git)

with open('README.md') as fr:
  readme = fr.read()

with open('LICENSE') as fl:
  license = fl.read()

url='https://github.com/i11/cosh',

setup(
  name='cosh',
  version=version,
  description='Container Shell',
  long_description=readme,
  long_description_content_type="text/markdown",
  author='Ilja Bobkevic',
  author_email='ilja@bobkevic.com',
  url=url,
  license=license,
  packages=find_packages(exclude=('tests', 'docs')),
  scripts=[
    'bin/cosh'
  ],
  install_requires=[
    'argparse==1.4.0',
    'requests==2.19.1',
    'google-auth==1.5.1',
    'natsort==5.3.3',
    'jsonpickle==0.9.6'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.6',
  ]
)
