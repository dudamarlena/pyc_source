"""Setup script for autosetup package.

Generated using autosetup on 2020-03-10 22:31:03.
"""

from setuptools import setup

setup(
    name="autosetup",
    version="2020.03.10.1.beta",
    url="https://github.com/diakovlev/autosetup",
    project_urls={},
    author="Daniil Iakovlev",
    author_email="daniil.iakovlev@gmail.com",
    license="MIT License",
    license_file="LICENSE",
    keywords="setuptools autosetup",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    description="Utility for creating setup.py script for packages",
    long_description_content_type="text/markdown",
    long_description=r"""# Autosetup

Utility for creating setup.py script and setup.cfg configuration for packages


## Usage

Create a PACKAGE.json file in the package directory root, 
see corresponding file of this package for reference.

Available fields are referenced below.


### Running the script

`from autosetup import make_setup`

`make_setup(PATH_TO_PACKAGE_ROOT, overwrite=True)`

* PATH_TO_PACKAGE_ROOT may be the full path or "." for current working directory
* overwrite: whether to overwrite existing setup.py or fail if it exists 


### Using Makefile


### Attribute Fields, Alternative Names and Extra Sources

Fields are case-insensitive.

* name - may also be placed as text in file "PACKAGE_NAME"
* version - may also be placed as text in file "VERSION"
   * ver
   * v
* url
* keywords
* description
* project_urls
   * urls
   * project urls
* author
* author_email
   * email
   * author email
* maintainer
* maintainer_email
* first_release
* long_description - *is pulled from any file starting with "README" by default*
* license - *is pulled from any file starting with "LICENSE" by default*
* python_requires - *defaults to current python version*
   * python
* extras_require
* tests_require
* exclude_packages - *defaults to `["tests*", "*.tests*"]`*
   * exclude
* scripts
* entry_points
* development_status - *see options below*
   * status
* classifier_license
* operating_systems
   * operating_system
   * operating system
   * operating systems
   * os
* environments
   * environment
* frameworks
   * framework
* intended_audiences
   * intended_audience
   * intended audience
   * intended audiences
   * audience
   * audiences
* topics
   * topic
* natural_languages
   * natural_language
   * natural language
   * natural languages


#### Development Status Options

* "Development Status :: 1 - Planning", also as:
   * 1
   * "1"
   * "1 - planning"
   * "planning"
   * "design"
* "Development Status :: 2 - Pre-Alpha", also as:
   * 2
   * "2"
   * "2 - pre-alpha"
   * "pre-alpha"
   * "dev"
   * "development"
* "Development Status :: 3 - Alpha", also as:
   * 3
   * "3"
   * "3 - alpha"
   * "alpha"
   * "test"
   * "testing"
* "Development Status :: 4 - Beta", also as:
   * 4
   * "4"
   * "4 - beta"
   * "beta"
   * "pre-release"
   * "staging"
* "Development Status :: 5 - Production/Stable", also as:
   * 5
   * "5"
   * "5 - production/stable"
   * "production/stable"
   * "release"
   * "production"
   * "stable"
* "Development Status :: 6 - Mature", also as:
   * 6
   * "6"
   * "6 - mature"
   * "mature"
* "Development Status :: 7 - Inactive", also as:
   * 7
   * "7"
   * "7 - inactive"
   * "inactive"
""",
    packages=[
        "autosetup"
    ],
    python_requires=">=3.8",
    install_requires=[]
)
