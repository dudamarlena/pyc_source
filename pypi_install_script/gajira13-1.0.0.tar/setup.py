from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

setup(
    name='gajira13',

    version='1.0.0',

    description='Monday time saver',

    # The project's main homepage.
    url='https://pypi.python.org/pypi/gajira13',

    # Author details
    author='LioK',
    author_email='1021ovk@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='jira',

    packages=find_packages(),

    install_requires=['jira'],

    entry_points={
        'console_scripts': [
            'gajira=gajira.gajira:main', #name=folder.file:function
        ],
    },
)
