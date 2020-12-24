from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='leanpubpy',
    version='0.0.0',
    description='Leanpub API Client',
    url='https://github.com/monzita/leanpubpy',
    author='Monika Ilieva',
    author_email='hidden@hidden.com',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3.6'
    ],

    keywords='number algoirthms',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'venv']),
)