import os
import sys
from distutils.sysconfig import get_python_lib

from setuptools import find_packages, setup


EXCLUDE_FROM_PACKAGES = ['mouser.bin']


version = '0.0.0'


setup(
    name='mouser',
    version=version,
    url='https://github.com/bristy/mouser',
    author='Brajesh Kumar',
    author_email='kbrajesh176@gmail.com',
    description=('A tool to save hours of developers'),
    license='Apache',
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    scripts=['mouser/bin/mouser-admin.py'],
    entry_points={'console_scripts': [
        'mouser-admin = mouser.core.management:execute_from_command_line',
    ]},
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
