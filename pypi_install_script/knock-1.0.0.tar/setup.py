from setuptools import *

kwargs = {
    "author" : "ShRP",
    "author_email" : "liberserpentis@gmail.com",
    "description" : "Trinity's hack emulation into Neo's computer",
    "entry_points" : {"console_scripts" : ["knock=knock.knock:main"]},
    "license" : "GPL v3",
    "name" : "knock",
    "packages" : ["knock"],
    "version" : "V1.0.0",
}

setup(**kwargs)
