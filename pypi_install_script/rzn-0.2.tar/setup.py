from setuptools import setup, find_packages
from os import path
setup(
   name="rzn",
   version='0.2',
   description="rzn - rsync/rclone git like push/pull wrapper",
   long_description="Rzn leverages rsync or rclone to synchronize your files. It searches for the configuration file .rzn in the current or parent directories like git so you can run rzn push / pull from any (sub)directory.",
   url="https://github.com/meeuw/rzn",
   packages=find_packages(exclude=[]),
   entry_points={
       "console_scripts": [
           "rzn=rzn.rzn:main",
       ]
   },
)
