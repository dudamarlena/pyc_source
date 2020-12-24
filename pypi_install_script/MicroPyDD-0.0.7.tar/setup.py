from os import path
from setuptools import setup

import src.micropydd as module

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='MicroPyDD',
    version=module.VERSION,
    description='MicroPyDD simplyfies managements of microservice boilerplates code',
    author="Danilo Delizia",
    author_email="ddelizia@gmail.com",
    package_dir={'': 'src'},
    packages=['micropydd'],
    install_requires=[
        'colorlog',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
