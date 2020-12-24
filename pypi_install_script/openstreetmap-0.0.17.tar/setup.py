# -*- coding: utf-8 -*-


from setuptools import setup, find_packages
from openstreemap import __version__

VERSION = __version__
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='openstreetmap',
    version=VERSION,
    description='OpenStreetMap coordinates',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache-2.0",
    author='galen',
    author_email='mywayking@icloud.com',
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    url='https://github.com/Mywayking/openstreetmap.git',
    keywords='openstreetmap',
    packages=find_packages(),
    install_requires=[
        'lxml',
        'requests',
    ],
    python_requires='>=3.4',
)
