import os
from setuptools import setup, find_packages


def read(file):
    return open(os.path.join(os.path.dirname(__file__), file)).read()


setup(
    name="Idmeneo_cdQa",
    version="0.0",
    author="Gabor Jonas",
    description="An End-To-End Closed Domain Question Answering System with sciBert",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    keywords="reading comprehension question answering deep learning natural language processing information retrieval bert",
    license="Apache-2.0",
    url="https://github.com/VincentVega002/Idomeneo_cdQa",
    packages=find_packages(),
    install_requires=read("requirements.txt").split(),
)
