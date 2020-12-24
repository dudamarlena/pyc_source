import os

from setuptools import setup


def read_file(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file_obj:
        return file_obj.read()


version = "0.17.1"
repo = "https://bitbucket.org/wareification/dcrate"
package_directory = os.path.dirname(os.path.abspath(__file__))

config = {
    "name": "dcrate",
    "version": version,
    "packages": [
        "dcrate",
    ],
    "install_requires": ["click==6.7"],
    "entry_points": {
        "console_scripts": [
            "dcrate=dcrate.cli:entry_point"
        ]
    },
    "author": "Jason Kaiser",
    "author_email": "wareification@programmer.net",
    "license": "BSD",
    "url": repo,
    "download_url": "{}/get/v{}.tar.gz".format(repo, version),
    "description": ("A collection of processes to prepare a software project" 
                    " for deployment"),
    "long_description": read_file(os.path.join(package_directory, "README.rst")),
    "classifiers": [
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.5",
        "Natural Language :: English",
        "Topic :: System :: Archiving",
        "Topic :: Software Development",
    ]
}

setup(**config)
