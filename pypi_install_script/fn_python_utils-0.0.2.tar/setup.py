#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages
from distutils.util import convert_path
import os

ver_path = convert_path(os.path.join("fn_python_utils", "VERSION.txt"))
with open(ver_path, "r", encoding="utf-8") as f:
    __version__ = f.read().strip()

readme_content = ""
'''
import os
project_root_folder_path = os.path.dirname(__file__)
with open(os.path.join(project_root_folder_path,"README.md"), "r", encoding="utf-8") as f:
    readme_content = f.read()
'''

setup(
    name='fn_python_utils',
    version=__version__,
    license="LGPL", 
    packages=["fn_python_utils"],
    author="François NOYEZ",
    author_email="francoisnoyez@gmail.com",
    description="Some python utilities.",
    #long_description=readme_content,
    url = "https://github.com/fnoyez/fn_python_utils",  
    download_url = 'https://github.com/fnoyez/fn_python_utils/archive/0.0.2.tar.gz', 
    keywords = ["Progress display",],
    install_requires=[
        'numpy',
        'scipy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)', 
        'Development Status :: 3 - Alpha', 
        'Intended Audience :: Developers',
        'Operating System :: Unix', 
    ],
    include_package_data=True, # Activate usage of the 'MANIFEST.in' file
)