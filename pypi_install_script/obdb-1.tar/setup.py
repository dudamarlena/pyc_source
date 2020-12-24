#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='obdb',
    version='1',
    url='https://github.com/bthate/obdb',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="OBDB contains database programs for the OB package.",
    long_description="""
Usage: obot [-b] [-k] [-p] [-z] [-x cmd] [options]

Options:
  --version        show program's version number and exit
  -h, --help       show this help message and exit
  -b               background mode.
  -d WORKDIR       set working directory.
  -m MODULES       modules to load.
  -x               execute command.
  -o OPTIONS       options to use.
  -k               read from previous kernel config.
  -p               prompt for initial values.
  -s               save configuration files.
  -z               disable shell.
  -l LEVEL         loglevel.
  --logdir=LOGDIR  directory to find the logfiles.
        
    """,
    long_description_content_type="text/markdown",
    license='Public Domain',
    install_requires=["ob"],
    zip_safe=True,
    packages=["obdb"],
    scripts=["bin/obdb"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
