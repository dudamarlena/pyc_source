# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 03:02:28 2019

@author: knbarnwal
"""

from distutils.core import setup
setup(
  name = 'data_normalization',         # How you named your package folder (MyLib)
  packages = ['data_normalization'],   # Chose the same as "name"
  version = 'v1.1',      # Start with a small number and increase it with every change you make
  license='mit',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'The Data normalization Library to easily find the min_max, z-score and decimal normalization of data file with multiple columns as input',   # Give a short description about your library
  author = 'Kumar Navin Barnwal',                   # Type in your name
  author_email = 'knbarnwal@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/user/navinbarnwal',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/navinbarnwal/normalization/archive/v1.0.tar.gz',    # I explain this later on
  keywords = ['min_max', 'normalization', 'z-score', 'decimal'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'numpy',
          "array",
          "random",
          "statistics"
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)