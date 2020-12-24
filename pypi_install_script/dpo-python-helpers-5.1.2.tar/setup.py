#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="dpo-python-helpers",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    url="https://bitbucket.org/dporganizer/dpo-python-helpers/src/develop/",
    author="Jim Brannlund",
    author_email="jim.brannlund@dporganizer.com",
    description="Python helpers for DPO-CLI",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "click<=7.0",
        "boto3==1.10.1",
        "requests<=2.22.0",
        "tabulate<=0.8.2",
    ],
    entry_points={
        "console_scripts": ["dev-env=dev_env.dev_env:main", "deploy=deploy.deploy:main"]
    },
)
