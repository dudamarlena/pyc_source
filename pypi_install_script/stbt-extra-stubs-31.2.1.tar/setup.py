# coding: utf-8

import setuptools


long_description = """\
# stbt-extra-stubs

* Copyright © 2018-2019 Stb-tester.com Ltd.

**Now renamed to stbt-premium-stubs:
<https://pypi.org/project/stbt-premium-stubs/>**
"""

setuptools.setup(
    name="stbt-extra-stubs",
    version="31.2.1",
    author="Stb-tester.com Ltd.",
    author_email="support@stb-tester.com",
    description="Stubs for Stb-tester's premium APIs - NOW RENAMED TO stbt-premium-stubs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://stb-tester.com",
    packages=["stbt"],
    classifiers=[
        # pylint:disable=line-too-long
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Testing",
    ],
    # I have only tested Python 2.7 & 3.6
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*",
)
