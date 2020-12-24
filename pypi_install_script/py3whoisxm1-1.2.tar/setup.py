from distutils.core import setup
from setuptools import setup,setuptools
import os 
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme_file:
    readme = readme_file.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='py3whoisxm1',
    version='1.2',
    packages=setuptools.find_packages(),
    include_package_data=True,
    long_description_content_type= 'text/markdown',
    long_description=open('README.md').read(),
    description = "A wrapper for the WhoisXML API service",
    author = "Vishnu Varthan Rao",
    author_email="vishnulatha006@gmail.com",
    url='https://github.com/VarthanV/pywhoisxml',
    install_requires=[
        "requests"
    ],
    license="MIT License",
    zip_safe=False,
    keywords='pywhoisxml,whoisxml,iplookup,ip ,geoip , domain reputation, website screenshot,lookup ',
     classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],

)