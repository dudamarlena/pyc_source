from setuptools import find_packages, setup
import sys

requirements = [
    'numpy>=1.13.0',
    'scipy',
    'pandas',
    'pyspark',
    'scikit-learn'
]

#public version 0.0.8
version = '0.0.8'

setup(
    name='search-tools',
    version=version,
    author="Michael Klear",
    author_email='fixityourself@fu.com',
    url='https://github.com/AlliedToasters/search-tools/archive/v0.0.8.tar.gz',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements
)
