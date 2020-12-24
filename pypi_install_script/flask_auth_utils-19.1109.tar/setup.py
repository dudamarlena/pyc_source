#!/usr/local/bin/python
from setuptools import setup, find_packages

setup(
    name="flask_auth_utils",
    description="An opinionated library for easily setting up auth using flask",
    version="19.1109",
    author="John Norwood",
    author_email="norwood.john.m@gmail.com",
    url="https://github.com/norwoodj/flask_auth_utils",
    download_url="https://github.com/norwoodj/jconfigure/archive/19.1109.tar.gz",
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask-login",
    ],
)
