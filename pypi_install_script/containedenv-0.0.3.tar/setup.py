import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


with open('requirements.txt') as requirements_file:
    install_requirements = requirements_file.read().splitlines()

setup(
    name="containedenv",
    version="0.0.3",
    author="Drew Stinnett",
    author_email="drew@drewlink.com",
    description=("Helper scripts for writing configuration files based on "
                 "environment variables"),
    install_requires=install_requirements,
    license="MIT",
    keywords="container docker",
    packages=['containedenv'],
    scripts=['scripts/containedenv-config-writer.py'],
    long_description_content_type="text/markdown",
    long_description=read('README.md'),
)
