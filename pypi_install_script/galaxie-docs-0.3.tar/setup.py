# -*- coding:utf-8 -*-
import os
from setuptools import setup

pre_version = "0.3"
if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    if os.environ.get('CI_JOB_ID'):
        version = os.environ['CI_JOB_ID']
    else:
        version = pre_version

with open('README.md') as f:
    long_description = f.read()

setup(name='galaxie-docs',
      version=version,
      description='Galaxie Docs is a survival ToolKit for bidirectional Markdown to HTML, HTML to Markdown conversion',
      long_description=long_description,
      long_description_content_type='text/markdown; charset=UTF-8',
      url='https://gitlab.com/Tuuux/galaxie-docs',
      author='Tuuux',
      author_email='tuxa@rtnp.org',
      license='GNU GENERAL PUBLIC LICENSE Version 3',
      packages=['GLXDocs'],
      entry_points={
          'console_scripts': [
              'glx-md2html = GLXDocs.__main__:md2html'
          ]
      },
      zip_safe=False,
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3 :: Only",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      setup_requires=[
          'green',
          'wheel'
      ],
      tests_require=[
          'wheel',
          'markdown',
          'Pygments'

      ],
      install_requires=[
          'wheel',
          'markdown',
          'Pygments'
      ])
