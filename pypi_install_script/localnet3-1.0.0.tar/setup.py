from setuptools import *

kwargs = {
    "author" : "ShRP",
    "author_email" : "liberserpentis@gmail.com",
    "description" : "ARP reconnaissance tool",
    "entry_points" : {"console_scripts" : ["localnet3=localnet3.localnet3:main"]},
    "license" : "GPL v3",
    "name" : "localnet3",
    "packages" : ["localnet3"],
    "version" : "V1.0.0",
}

setup(**kwargs)
