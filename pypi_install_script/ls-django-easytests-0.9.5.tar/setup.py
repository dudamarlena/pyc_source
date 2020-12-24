from setuptools import setup, find_packages
import os

import djeasytests

version = djeasytests.get_version()

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

CLASSIFIERS = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
]

setup(
    name='ls-django-easytests',
    version=version,
    description='Modified test utils from django-cms as a own module',
    long_description=(read('README.rst') + '\n\n' +
                      read('HISTORY.rst')),
    author='Scott Sharkey',
    author_email='ssharkey@lanshark.com',
    url='http://github.com/lanshark/ls-django-easytests/',
    download_url='https://github.com/lanshark/ls-django-easytests/tarball/' + version,
    packages=find_packages(),
    classifiers=CLASSIFIERS,
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'docopt',
        'dj-database-url'
    ]
)
