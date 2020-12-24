from os import path
from setuptools import setup

import src.micropydd_restplus as module

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='MicroPyDD-restplus',
    version=module.VERSION,
    description='MicroPyDD wrapper for Flask-Restplus',
    author="Danilo Delizia",
    author_email="ddelizia@gmail.com",
    package_dir={'': 'src'},
    packages=[
        'micropydd_restplus',
        'micropydd_restplus.namespaces',
    ],
    install_requires=[
        'micropydd',
        'flask',
        'flask-restplus',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
