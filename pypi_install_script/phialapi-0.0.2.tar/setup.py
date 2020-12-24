import os

from setuptools import setup, find_packages

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name='phialapi',
    version='0.0.2',
    description='Simple django-rest implementation to store files in a plethora of storage engines',
    long_description=(read('README.md') + '\n\n' +
                      read('HISTORY.md') + '\n\n' +
                      read('AUTHORS.md')),
    url='http://github.com/derek-adair/phial-api',
    license='MIT',
    author='Derek Adair',
    author_email='d@derekadair.com',
    py_modules=['phial_api'],
    packages=find_packages(exclude='demo'),
    include_package_data=True,
    zip_safe=False,
    install_requires=['djangorestframework', 'django'],
)
