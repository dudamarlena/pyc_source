from setuptools import setup, find_packages

setup(
    name="some_package_andre_317",
    description="Package to demonstrate how to use pypi, pytest, GitHub and \
        CircleCI",
    version="1.0.0",
    author="Andre Fellipe",
    author_email="andrefellipern@gmail.com",
    url="http://andrefellipe.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
