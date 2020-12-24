#! /usr/bin/env python3
from setuptools import setup, find_packages
from pathlib import Path


setup(
    name='apaho',
    description='Asynchronous wrapper for paho.mqtt',
    long_description=Path('README.md').read_text(),
    long_description_content_type="text/markdown",
    author='Vladimir Shapranov',
    author_email='equidamoid@gmail.com',
    url='https://github.com/Equidamoid/apaho',
    packages=find_packages(),
    install_requires=['paho-mqtt'],
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
