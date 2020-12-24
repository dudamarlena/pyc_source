from setuptools import setup

setup(
    name='flightplan',
    packages = ['flightplan'],
    version='0.6',
    install_requires=[
        'pyrebase'
    ],
    description = 'A procedure manager for Rowley Group',
    author = 'Mohamad Mohebifar',
    author_email = 'mmohebifar@mun.ca',
    url = 'https://github.com/mohebifar/flightplan', # use the URL to the github repo
    download_url = 'https://github.com/mohebifar/flightplan/tarball/0.1', # I'll explain this in a second
    keywords = ['flightplan', 'rowley'], # arbitrary keywords
    classifiers = [],
)
