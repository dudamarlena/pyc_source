from setuptools import *

kwargs = {
    "author" : "ShRP",
    "author_email" : "liberserpentis@gmail.com",
    "description" : "File statistics script",
    "entry_points" : {"console_scripts" : ["pystat3=pystat3.pystat3:main"]},
    "license" : "GPL v3",
    "name" : "pystat3",
    "packages" : ["pystat3"],
    "version" : "V1.0.0",
}

setup(**kwargs)
