# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 09:54:44 2019

@author: vikash
"""

from distutils.core import setup
setup(
  name = 'bin_boundary',         # How you named your package folder (MyLib)
  packages = ['bin_boundary'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This package perform one of the smoothing method of Binning method(Bin by Boundaries).It ask for file name and column name ',   # Give a short description about your library
  author = 'VIKASH SINGH',                   # Type in your name
  author_email = 'vikashlikes18@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Vikash29Singh/bin_boundary.git',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Vikash29Singh/bin_boundary/archive/v0.1.tar.gz',    # I explain this later on
  keywords = ['bin', 'boundary', 'python'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'numpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which python versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
