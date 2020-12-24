import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='jwt-i2tic',
    version='0.2.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='Simple JWT.',
    long_description=README,
    url='https://www.example.com/',
    author='David M y Oscar Garcia',
    author_email='d.martin@i2tic.com',
    classifiers=[
     
    
    ],
)
