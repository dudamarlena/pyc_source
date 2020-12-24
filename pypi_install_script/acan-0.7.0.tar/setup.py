#!/usr/bin/env python3

from setuptools import setup
from codecs import open

setup(
    name='acan',
    packages=['acan'],
    version='0.7.0',
    description='Maths around brewing',
    long_description=open('README.rst',encoding='utf-8').read(),
    author='José Lopes de Oliveira Jr.',
    license='MIT License',
    url='https://github.com/bierminen/acan',
    keywords=['acan','beer','equation','brewery'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ]
)
