from setuptools import setup, find_packages
import sys, os

import ktextsurfacewriter

setup(name='KTextSurfaceWriter',
      py_modules=['ktextsurfacewriter',],
      version=ktextsurfacewriter.__version__,
      description=ktextsurfacewriter.__description__,
      long_description=open(os.path.join("docs", "README.txt")).read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: GNU General Public License (GPL)",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 2.5",
                   "Topic :: Games/Entertainment",
                   "Topic :: Multimedia :: Graphics",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   "Topic :: Software Development :: User Interfaces",
                   ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python pygame text surface ktextsurfacewriter library',
      author='Keul',
      author_email='lucafbb@gmail.com',
      url='http://keul.it/develop/python/ktextsurfacewriter/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
