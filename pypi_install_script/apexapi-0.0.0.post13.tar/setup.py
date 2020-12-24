"""
Setup.py for ApexAPI
"""

from setuptools import setup
version = "0.0.0-13" #NOTE: please blame pypi for the weird version numbers...

setup(
    name='apexapi',
    version=version,
    description="Apex is a modern microservice framework written in Python.",
    url='https://gitlab.com/apexapi/apexapi',
    author='Dan Sikes',
    author_email='dansikes7@gmail.com',
    keywords='python, framework, microservices, modern, api',

    packages=[
        'apexapi',
        'apexapi.core.handlers.apex',
        # 'apexapi.core.templates'
    ],

    install_requires=[
        'click',
        'pyaml',
        'munch',
        'werkzeug',
        'requests'
    ],

    entry_points = {
        'console_scripts': ['apex=apexapi:main'],
    },
    
    project_urls={
        'Source': 'https://gitlab.com/dsikes/apex',
    },
)