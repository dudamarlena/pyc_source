from os import chdir, path, pardir
from setuptools import setup, find_packages

with open(path.join(path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

#Allow setup.py to be run from any path
chdir(path.normpath(path.join(path.abspath(__file__), pardir)))

setup(
    name="darwin-shared",
    packages=find_packages(),
    include_package_data=True,
    description="Shared libraries for microservices",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT License",
    author="Developers",
    author_email="developers@starkbank.com",
    keywords=["darwin"],
    install_requires=[
        "pytz==2019.3",
        "starkbank-ecdsa~=0.1.6",
        "GoogleAppEngineCloudStorageClient==1.9.22.1"
    ],
    version="0.2.69"
)
