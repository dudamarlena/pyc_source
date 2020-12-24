#coding=utf-8
from setuptools import setup, find_packages

setup(
    name = "CommandUI",
    version = "1.0.7",
    keywords = ("pip", "commandline","console", "UI"),
    description = "ui tools for console",
    long_description = "ui tools for console",
    license = "MIT Licence",

    url = "https://coding.net/u/lin3x/p/CUI/git",
    author = "lishion",
    author_email = "544670411@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['prompt_toolkit>=2.0.4']
)