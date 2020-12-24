from setuptools import *

kwargs = {
    "author" : "ShRP",
    "author_email" : "liberserpentis@gmail.com",
    "description" : "Traverse directories with pywalk",
    "entry_points" : {"console_scripts" : ["pywalk3=pywalk3.pywalk3:main"]},
    "license" : "GPL v3",
    "name" : "pywalk3",
    "packages" : ["pywalk3"],
    "version" : "V1.0",
}

setup(**kwargs)
