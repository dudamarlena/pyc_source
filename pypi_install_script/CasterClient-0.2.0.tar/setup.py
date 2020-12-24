#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name = "CasterClient",
    version = "0.2.0",
    keywords = ("pip", "Mock_Server", "Caster_Union", "caster"),
    description = "client of Caster_Union",
    long_description = "It's the client of Caster_Union, which is a MockServer framework.",
    license = "Yitu Licence",

    author = "zhenyu.yin",
    author_email = "823243347@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)