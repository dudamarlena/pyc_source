import os

from setuptools import setup


def read_file(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file_obj:
        return file_obj.read()


version = "0.19.0"
repo = "https://bitbucket.org/wareification/synthpressure"
package_directory = os.path.dirname(os.path.abspath(__file__))

config = {
    "name": "synthpressure",
    "version": version,
    "packages": [
        "synthpressure",
        "synthpressure.assets",
        "synthpressure.backend",
        "synthpressure.content",
        "synthpressure.engine",
        "synthpressure.physics",
        "synthpressure.time",
        "synthpressure.utility",
    ],
    "install_requires": ["pyglet==1.2.4"],
    "author": "Jason Kaiser",
    "author_email": "wareification@programmer.net",
    "license": "BSD",
    "url": repo,
    "download_url": "{}/get/v{}.tar.gz".format(repo, version),
    "description": "An engineer's attempt at a game engine.",
    "long_description": read_file(os.path.join(package_directory, "README.rst")),
    "classifiers": [
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.5",
        "Natural Language :: English",
        "Topic :: Games/Entertainment",
    ]
}

setup(**config)
