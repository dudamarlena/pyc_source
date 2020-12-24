import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


with open('requirements.txt') as requirements_file:
    install_requirements = requirements_file.read().splitlines()

setup(
    name="azurectx",
    version="0.0.2",
    author="Drew Stinnett",
    author_email="drew@drewlink.com",
    description=("Switch between default Azure subscriptions"),
    install_requires=install_requirements,
    license="BSD",
    keywords="azure az",
    scripts=['scripts/azurectx'],
    long_description_content_type="text/markdown",
    long_description=read('README.md'),
)
