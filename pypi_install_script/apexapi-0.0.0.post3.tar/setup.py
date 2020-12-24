"""
Setup.py for ApexAPI
"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
version = "0.0.0-3" #NOTE: please blame pypi for the weird version numbers...

setup(
    name='apexapi',
    version=version,
    description="Apex is a modern microservice framework written in Python.",
    url='https://gitlab.com/apexapi/apexapi',
    author='Dan Sikes',
    author_email='dansikes7@gmail.com',
    keywords='python, framework, microservices, modern, api',

    packages=[
        'src',
        'src.core.handlers.apex'
    ],

    install_requires=[
        'click',
        'pyaml',
        'munch',
        'werkzeug',
        'requests'
    ],

    entry_points = {
        'console_scripts': ['apex=src:main'],
    },
    
    project_urls={
        'Source': 'https://gitlab.com/dsikes/apex',
    },
)