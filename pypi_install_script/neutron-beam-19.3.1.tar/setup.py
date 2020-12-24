import os

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


def get_readme():
  readme = os.path.join(here, 'README.md')
  with open(readme, 'r') as fh:
    return fh.read()


def get_version():
  init = os.path.join(here, 'nbeam', '__init__.py')
  with open(init, 'r') as fh:
    version = fh.readline().split('=')[-1]
    version = version.replace("\n", "")
    version = version.replace("\r", "")
    version = version.replace("'", "")
    version = version.replace(" ", "")
    version = version.replace('"', "")
    return version


setup(
    name='neutron-beam',
    version=get_version(),
    description='Client to beam files to and from neutron64.com',
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    url='https://www.neutron64.com',
    author='Paul Bailey',
    author_email='paul@neutron64.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='development',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    setup_requires=['setuptools>=38.6.0'],
    install_requires=[
        'binaryornot',
        'click >= 6.7, < 7',
        'netifaces',
        'pyjwt >= 1.5.3, < 2',
        'requests',
        'terminado',
        'tornado >= 5.0.2, < 6',
    ],
    extras_require={},
    package_data={},
    entry_points={
        'console_scripts': ['nbeam=nbeam.run:main',],
    },
)
