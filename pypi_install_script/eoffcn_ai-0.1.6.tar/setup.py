import sys

from setuptools import setup, find_packages

import eoffcn_ai

if sys.version_info < (3, 5):
    sys.exit('Python 3.5 or greater is required.')

with open('README.rst', encoding="utf8") as fp:
    readme = fp.read()

setup(
    name='eoffcn_ai',
    version=eoffcn_ai.__version__,
    description='eoffcn ai api.',
    long_description=readme,
    author='PuKun',
    author_email='pukun@offcn.com',
    maintainer='PuKun',
    maintainer_email='pukun@offcn.com',
    packages=find_packages(),
    include_package_data=True,
    # package_data={'': ['*.jar', '*.php', '*.json', '*.bat', '*.dll', '*.exe']},
    install_requires=['numpy', 'opencv-python', 'pandas', 'pillow', 'requests'],
    platforms=['any'],
    classifiers=[]
    )
