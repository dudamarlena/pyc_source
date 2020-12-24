import codecs
import os
import sys

try:
	from setuptools import setup, find_packages
except:
	from distutils.core import setup

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname),encoding='utf-8').read()

setup(
    name = "cycuCourse",
    version = "1.0.3",
    description = "A Auxiliary package for CYCU course selection system.",
    long_description = read("README.md"),
    long_description_content_type='text/markdown',
    classifiers =
	[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Chinese (Traditional)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=
	[
        'requests>=2.18.4',
    ],
    keywords = "CYCU Course Selection 中原 選課",
    author = "y252328",
    author_email = "y252328@gmail.com",
    url ="https://github.com/y252328/CYCU-Course-Selection-Helper",
    license = "MIT",
    packages = find_packages(),
    entry_points={
        'console_scripts': [
            'selection_helper=cycuCourse.selection_helper:cli',
        ],
    },
    include_package_data= True,
    zip_safe= False,
    project_urls={
        'Bug Reports': 'https://github.com/y252328/CYCU-Course-Selection-Helper/issues',
        'Source': 'https://github.com/y252328/CYCU-Course-Selection-Helper',
    },
)