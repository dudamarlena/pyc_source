from setuptools import setup
from os import environ

VERSION= environ.get('NC5NG_VERSION', "0.0.4")

PKG_INFO= {
    'name':"nc5ng",
    'version':VERSION,
    'description': "Python Library for Geodetic Datum Transformations",
    'long_description': """Geodetic Datum Transformations for GIS Analysis, source data from transformation data provided by nadcon5-ng (https://nc5ng.org/project/nadcon5-ng)

For More Information See: https://nc5ng.org/projects/nc5ng-python

For Documentation See: https://py.docs.nc5ng.org
""",
    'author':"Andrey Shmakov",
    'author_email':"akshmakov@gmail.com",
    'url':"https://nc5ng.org/projects/nc5ng-python",
    'download_url':"https://github.com/nc5ng/nc5ng-python",
    'install_requires':[
        'nc5ng-core >=0.0.4',
        'nc5ng-common >=0.0.4'
        ],
    'license':"MIT"
}

setup(**PKG_INFO)
