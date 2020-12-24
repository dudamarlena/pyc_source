from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='numerix',
    version='0.0.0',
    description='Implementation of some numerical algorithms',
    url='https://github.com/monzita/numerix',
    author='Monika Ilieva',
    author_email='hidden@hidden.com',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: Apache Software License',
      'Programming Language :: Python :: 3.6'
    ],

    keywords='number algoirthms',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'venv']),
)