import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='ECAuth0Backend',
    version='0.2.2',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Django app to authenticate with code or JWT for DjangoRestFramework',
    long_description=README,
    url='https://ephemerecreative.ca',
    author='Raphaël Titsworth-Morin',
    author_email='raphael@ephemerecreative.ca',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)