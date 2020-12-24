from os import path
from setuptools import setup

import src.micropydd_firestore as module

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='MicroPyDD-firestore',
    version=module.VERSION,
    description='MicroPyDD wrapper for Google firestore',
    author="Danilo Delizia",
    author_email="ddelizia@gmail.com",
    package_dir={'': 'src'},
    packages=[
        'micropydd_firestore',
    ],
    install_requires=[
        'micropydd',
        'google-cloud-firestore',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
