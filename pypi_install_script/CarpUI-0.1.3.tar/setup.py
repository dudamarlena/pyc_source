# -*- coding: utf-8 -*- 

from setuptools import setup


setup(
    name='CarpUI',
    python_requires='>=3.7.1',
    version="0.1.3",
    description="UI testing automation platform.",
    author="carp",
    packages=[
        'carp_ui'
    ],
    install_requires=[
        'selenium==3.141.0'
    ],
)
