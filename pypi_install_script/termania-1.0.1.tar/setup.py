from os.path import abspath, dirname, join

from setuptools import setup

here = abspath(dirname(__file__))

packages = ["termania"]

requires = ["bs4>=0.0.1", "beautifulsoup4>=4.8.2", "requests>=2.22.0"]

about = {}
with open(join(here, "termania", "__version__.py"), "r") as fh:
    exec(fh.read(), about)

with open(join(here, "README.md"), "r") as fh:
    readme = fh.read()

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    packages=packages,
    include_package_data=True,
    python_requires='~=3.5',
    install_requires=requires,
    license=about["__license__"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    project_urls={"Source": about["__url__"]},
)
