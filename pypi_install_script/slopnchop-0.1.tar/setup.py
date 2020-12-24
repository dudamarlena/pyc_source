import os
from setuptools import setup, find_packages

setup(
    name='slopnchop',
    version="v0.1",
    packages=find_packages(),
    author_email = 'kiefl.evan@gmail.com',
    author = 'Evan Kiefl',
    url = 'https://github.com/ekiefl/slopnchop',
    install_requires=open('requirements.txt','r').readlines(),
    scripts = [os.path.join('bin', 'slopnchop')],
)
