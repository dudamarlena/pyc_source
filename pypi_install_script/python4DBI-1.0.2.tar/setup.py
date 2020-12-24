import pathlib
from setuptools import setup, find_packages

BASE_DIR = pathlib.Path(__file__).parent

README = (BASE_DIR / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="python4DBI",
    version="1.0.2",
    description="The python 4DBI",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/marcianobarros/python4dbi",
    author="Marciano Barros",
    author_email="marciano.barros@pestana.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        'Topic :: Database',
        'Intended Audience :: Developers',
        'Development Status :: 5 - Production/Stable',
    ],
    packages=["python4DBI"],
    include_package_data=True,
    install_requires=["texttable"],
    setup_requires=['wheel'],
    keywords='datababase drivers DBI dbi 4D 4d',
)

