from setuptools import setup, find_packages
from os.path import join, dirname, basename



with open('README.rst', 'r') as file:
    readme = file.read()


setup_requirements = ["pip>=18.1"]
requirements = [
  'paramiko',
  'torch'
]


authors = [
    "A. Makarov"
]

setup(
    author = authors,
    author_email = "makarov.alxr@yandex.ru",
    classifiers = [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Natural Language :: Russian",
        "Programming Language :: Python :: 3.7",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    description = "A pytorch dataset that allows you to iterate the data that is on the remote machine without having to copy all the data.",
    name = "remtorch",
    long_description = readme,
    long_description_content_type = 'text/x-rst',
    python_requires=">=3.6",
    license = "MIT license",
    packages = find_packages(),
    setup_requires = setup_requirements,
    install_requires = requirements,
    version = "0.0.2",
    url = "https://github.com/NRshka/remote-dataset",
)