import setuptools
import io
import re

with io.open("lhcsmapi/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lhcsmapi",
    version=version,
    author="TE-MPE",
    author_email="lhc-signal-monitoring@cern.ch",
    description="A package with an API for signal access and processing for the LHC Signal Monitoring project.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.cern.ch/LHCData/lhc-sm-api",
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
