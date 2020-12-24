# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md', 'r') as rf:
    README = rf.read()

with open('VERSION.txt', 'r') as vf:
    VERSION = vf.read()

install_requirements = [
    'torch>=1.4',
    'torchvision>=0.5',
    'numpy>=1.18',
    'sentencepiece>=0.1.8',
    'gin-config>=0.3.0',
    'Click>=7.0',
    'ray>=0.9.0.dev0',
    'apex>=0.1',
    'tensorboardX>=2.0',  # Unmarked Ray dependency
    'requests>=2.23.0',  # Unmarked Ray dependency
    'pandas>=1.0.1',  # Unmarked Ray dependency
    'tabulate>=0.8.6',  # Unmarked Ray dependency
]

setup(
    name='pele',
    version=VERSION,
    description='Video Description/Captioning Framework',
    long_description=README,
    long_description_content_type='text/markdown',
    author='David Chan',
    author_email='davidchan@berkeley.edu',
    url='https://github.com/DavidMChan/pele',
    license='Apache-2',
    install_requires=install_requirements,
    entry_points={'console_scripts': [
        'pele=pele.run:main_fn',
    ]},
    packages=find_packages(exclude=['example', 'scripts']),
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.6',
  ],
)
