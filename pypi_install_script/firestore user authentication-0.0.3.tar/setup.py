#!/usr/bin/env python

from distutils.core import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='firestore user authentication',
        version='0.0.3',
        license="GNU",
        description='Firestore user authentication function for Python',
        author='Ryan Chen',
        author_email='ryanjchen2@gmail.com',
        url='https://github.com/fatcat2/firestore-auth',
        packages=['firestore_auth'],
        keywords=["google", "cloud", "firestore", "authentication"],
        install_requires=["google-cloud-firestore"],
        long_description=open("README.md").read(),
        long_description_content_type='text/markdown',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'Programming Language :: Python :: 3.7',
        ],
)
