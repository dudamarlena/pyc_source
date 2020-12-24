""" setup.py """
from setuptools import setup

setup(
    name='threegen',
    version='0.2.4',
    author='Ian Brault',
    author_email='ian.brault@engineering.ucla.edu',
    packages=['threegen'],
    scripts=['bin/threegen'],
    url='https://pypi.org/project/threegen/',
    license='GPLv3',
    description='a three.js project template generator',
    long_description=open('README.rst').read(),
    zip_safe=False,
)
