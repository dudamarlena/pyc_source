# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 15:53:27 2020

@author: LearnLeap
"""

from distutils.core import setup
setup(
  name = 'Phygital',         # How you named your package folder (MyLib)
  packages = ['Phygital'],   # Chose the same as "name"
  version = '0.5',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This is the library for hardware interactions',   # Give a short description about your library
  author = 'TechClub',                   # Type in your name
  author_email = 'renuka.angole@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/RenukaAngole1/phygital',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/RenukaAngole1/phygital/archive/0.5.tar.gz',    # I explain this later on
  keywords = ['Hardware', 'Wireless', 'Phygital'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
           'pyserial',
          'requests',
          'pyttsx3',
          'SpeechRecognition',
          'python-vlc',
          'pygame',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.7',
  ],
)