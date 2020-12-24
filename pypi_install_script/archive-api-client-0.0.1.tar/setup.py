import setuptools

requires = []
packages = ["archive_client"]

requires.extend([
    "requests==2.22.0",
    "Beautifulsoup4==4.8.0",
])

setuptools.setup(
    name="archive-api-client",
    version="0.0.1",
    description=("Python wrapper for the CNX Archive API"
                 "(http://archive.cnx.org)"),
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    license="AGPLv3",
    author="m1yag1",
    author_email="mike.arbelaez@rice.edu",
    url="",
    packages=packages,
    package_dir={"": "src"},
    install_requires=requires,
    classifiers=[
    ],
    extras_require={
    },
)
