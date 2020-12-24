from setuptools import setup
from os import environ
VERSION= environ.get('NC5NG_VERSION', "0.0.4")
PKG_INFO= {
    'packages':['nc5ng.gmt', 'nc5ng.types'],
    'name':"nc5ng-common",
    'version':VERSION,
    'description': "Python common packages for nc5ng",
    'long_description': """Common utilities shared by other packages. 
    installed by default with target `nc5ng`

For More Information See: https://nc5ng.org/projects/nc5ng-python

For Documentation See: https://docs.nc5ng.org/latest
""",
    'author':"Andrey Shmakov",
    'author_email':"akshmakov@gmail.com",
    'url':"https://nc5ng.org/projects/nc5ng-python",
    'download_url':"https://github.com/nc5ng/nc5ng-python-common",
    'install_requires':[
        'numpy'
        ],
    'license':"MIT"
}

setup(**PKG_INFO)
