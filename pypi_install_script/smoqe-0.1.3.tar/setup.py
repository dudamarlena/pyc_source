from setuptools import setup, find_packages
setup(
    name="smoqe",
    version="0.1.3",
    packages=find_packages(),
#    py_modules = [],
# TBD:
#    entry_point={
#        'console_scripts': [
#             'smoqer = smoq.query:main'
#        ]
#    },
    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires =['docutils>=0.3'],
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
    },
    # metadata for upload to PyPI
    author="Dan Gunter",
    author_email="dkgunter@lbl.gov",
    description="Simple MongoDB Query Engine (SMoQE)",
    license="LGPL",
    keywords="MongoDB",
    url="https://github.com/dangunter/smoqe/",
    # could also include long_description, download_url, classifiers, etc.
)
