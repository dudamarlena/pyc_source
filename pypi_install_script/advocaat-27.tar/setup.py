#!/usr/bin/python3

""" setup.py """

from setuptools import setup

with open('README') as file:
    long_description = file.read()

setup(
    name='advocaat',
    version='27',
    url='https://bitbucket.org/bthate/advocaat',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="gif toedienen is poging tot moord",
    long_description=long_description,
    license='Public Domain',
    install_requires=["zelf"],
    scripts=["bin/advocaat"],
    packages=["advocaat"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
