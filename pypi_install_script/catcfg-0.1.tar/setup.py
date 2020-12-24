# -*- coding: utf-8 -*-
# @Description: 
# @Author: kowhoy
# @Date:   2020-04-29 10:27:46
# @Last Modified by:   zhouke
# @Last Modified time: 2020-04-29 15:00:17
from setuptools import setup, find_packages

setup(
    name="catcfg",
    version="0.1",
    packages=find_packages(),

    description="catcfg: manage config data easily",
    author="kowhoy",
    author_email="kowhoy@163.com",
    install_requires=["pylsy", "click"],
    license="GPL",
    keywords=["catcfg", "catconfig"],
    platforms="Independant",
    url="https://kowhoy.com",
    entry_points={
        "console_scripts":[
            "catcfg=cfg.catconfig:cli"
        ]
    }
)