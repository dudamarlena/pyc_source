#/usr/bin/env python
# coding: utf8
from setuptools import setup, find_packages
from farbox import version

setup(
    name='farbox',
    version=version,
    description='FarBox',
    author='Hepochen',
    author_email='hepochen@gmail.com',
    include_package_data=True,
    packages=find_packages(),

    install_requires = [
        'psutil',
        'ujson',
        'pyssdb==0.4.2',
        'cryptography', # ==2.3
        'enum',
        'setuptools>=40.0.0'
    ],

    entry_points={
        'console_scripts':[
            #'xx = package_name.xx:main',
        ]
    },

    platforms = 'linux',
)