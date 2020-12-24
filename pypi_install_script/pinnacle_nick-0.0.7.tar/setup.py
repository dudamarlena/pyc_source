
from setuptools import setup, find_packages
from pinnacle import __version__

setup(
    name="pinnacle_nick",
    version=__version__,
    author="Nick Georgiadis",
    author_email="nickgeo_@hotmail.com",
    description="Pinnacle Nick API Python wrapper",
    url="https://github.com/rozzac90/pinnacle",
    packages=find_packages(),
    install_requires=[line.strip() for line in open("requirements.txt")],
    long_description=open('README.md').read(),
    tests_require=['pytest'],
)
