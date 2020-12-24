#coding:utf-8
#package project
from setuptools import setup, find_packages
setup(
name="Firstmysite_Jia",
version="1.0.4",
author="Darren_liu",
author_email="Darren_Liu@syscom.com.tw",
#自動尋找帶有 __init__.py 的資料夾
packages=find_packages(exclude=["logs"]),
install_requires = ['django==2.2.6'],
description = "ap monitor system",
#單獨的一些py指令碼,不是在某些模組中
scripts = ["Firstmysite_Jia\manage.py", "settings.py", 
"uwsgi.py", "__init__.py"],
#靜態檔案等，配合MANIFEST.in (package_data 引數不太好使)
include_package_data = True,

)