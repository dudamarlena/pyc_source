from setuptools import setup, find_packages
import pack2048
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='pack2048',
    version=pack2048.__version__,
    packages=find_packages(),
    author="Jérémy Duron",
    author_email="jlmncddgg@gmail.com",
    description="Un module pour résoudre le 2048",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    #url='http://github.com/',
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers.
    #Development Status :: 1 - Planning
    #Development Status :: 2 - Pre-Alpha
    #Development Status :: 3 - Alpha
    #Development Status :: 4 - Beta
    #Development Status :: 5 - Production/Stable
    #Development Status :: 6 - Mature
    #Development Status :: 7 - Inactive
    classifiers=[
        "Development Status :: 6 - Mature",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python :: 3.7",
    ],
 
)