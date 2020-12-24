import ast
from setuptools import setup, find_packages


def get_version(file_name, version_name="__version__"):
    with open(file_name) as f:
        tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                if node.targets[0].id == version_name:
                    return node.value.s
    raise ValueError("Unable to find an assignment to the variable {}".format(version_name))


class About(object):
    NAME = "get-mnist"
    VERSION = get_version("mnist/__init__.py")
    AUTHOR = "blester125"
    EMAIL = "{}@gmail.com".format(AUTHOR)
    URL = "https://github.com/{}/{}".format(AUTHOR, NAME)
    DL_URL = "{}/archive/{}.tar.gz".format(URL, VERSION)
    LICENSE = "MIT"
    DESCRIPTION = "Low Dependency Fetching of MNIST dataset"


ext_modules = []


setup(
    name=About.NAME,
    version=About.VERSION,
    description=About.DESCRIPTION,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author=About.AUTHOR,
    author_email=About.EMAIL,
    url=About.URL,
    download_url=About.DL_URL,
    license=About.LICENSE,
    packages=find_packages(),
    package_data={"mnist": [],},
    include_package_data=True,
    install_requires=["six", "numpy",],
    extras_require={"test": ["pytest", "mock"],},
    keywords=["MNIST", "Machine Learning", "Datasets"],
    ext_modules=ext_modules,
    entry_points={"console_scripts": ["mnist=mnist.mnist:main",],},
    classifiers={
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
    },
)
