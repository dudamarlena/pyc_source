from setuptools import setup

name = 'goopy'
version = '0.3.2'
description = 'A simple compatibility layer between Go and Python'
author = 'Matt C. (fluofoxxo)'
author_email = 'me@fluofoxxo.pw'
packages = ['goopy']
keywords = 'goopy go golang python compatibility layer wrapper'.split(' ')
download_url = 'https://github.com/fluofoxxo/goopy/tarball/master/'

if __name__ == "__main__":
    setup(**{_name: _loc for _name, _loc in globals().items() if _name != "setup" and _name[0] != "_"})
