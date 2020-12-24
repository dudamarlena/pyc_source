import os, sys
from distutils.core import setup
from distutils.dir_util import copy_tree, remove_tree

def get_sub_packages(root):
    packages = [os.path.basename(root)]
    for r, d, f in os.walk(root):
        packages += [os.path.join(r,dx).replace('\\','.') for dx in d]
    return packages

name = 'dragon'

setup(
    name=name.capitalize(),
    version='0.0.5',
    author='Ofer Sadan',
    author_email='ofersadan85@gmail.com',
    packages=get_sub_packages(name),
    url=f'http://pypi.python.org/pypi/{name}/',
    license='LICENSE.txt',
    description='General utilities and useful extensions for other packages',
    long_description=open('README.txt').read(),
)
