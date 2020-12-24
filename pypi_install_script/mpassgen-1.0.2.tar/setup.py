#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright © 2020 Aleksandr Suvorov
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# -----------------------------------------------------------------------------
# Aleksandr Suvorov (hackband)
# Yandex Money: https://money.yandex.ru/to/4100110928527458
# Sberbank Russia: 4276 4417 5763 7686
# PayPal: paypal.me/py2ru
# Email: myhackband@gmail.com
# -----------------------------------------------------------------------------
from setuptools import setup, find_packages
from os.path import join, dirname

PACKAGE = "mpassgen"
VERSION = __import__(PACKAGE).__version__
AUTHOR = 'Aleksandr Suvorov'
AUTHOR_EMAIL = "myhackband@gmail.com"
DESCRIPTION = "Password Generator | Author: Aleksandr Suvorov " \
              "| Site: https://github.com/hackband/mypassgen " \
              "| Email: myhackband@gmail.com | Donate: 4276 4417 5763 7686"
NAME = "mpassgen"
URL = "https://github.com/hackband/mypassgen"
LICENSE = 'MIT'
PLATFORM = ['Linux, Windows']
LONG_DESCRIPTION = open(join(dirname(__file__), 'README.txt')).read()
INSTALL_REQUIRES = ['pyside2']
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: X11 Applications :: Qt',
    'License :: OSI Approved :: MIT License',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3',
]
ENTRY_POINTS = {
    'console_scripts':
        ['termpassgen = mpassgen.term_pass_gen:main'],
    'gui_scripts':
        ['mpassgen = mpassgen.my_pass_gen:main']
}
KEYWORDS = [
    'mpassgen',
    'password generator',
]
setup(
    name=NAME,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    description=DESCRIPTION,
    version=VERSION,
    license=LICENSE,
    platforms=PLATFORM,
    packages=find_packages(),
    long_description=LONG_DESCRIPTION,
    entry_points=ENTRY_POINTS,
    install_requires=INSTALL_REQUIRES,
    include_package_data=True,
    zip_safe=False,
    keywords=KEYWORDS
)
