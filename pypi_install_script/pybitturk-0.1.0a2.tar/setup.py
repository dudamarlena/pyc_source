from setuptools import setup

import pybitturk

with open("README.md", "r") as f:
    README = f.read()

with open("requirements.txt", "r") as f:
    DEPS = f.readlines()

with open("dev.requirements.txt", "r") as f:
    TEST_DEPS = f.readlines()

GITHUB_RELEASE_URL = "https://github.com/erayerdin/pybitturk/archive/v{}.tar.gz"

setup(
    name="pybitturk",
    version=pybitturk.__version__,
    description="pybitturk is a Python implementation of BitTurk API.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/erayerdin/pybitturk",
    download_url=GITHUB_RELEASE_URL.format(pybitturk.__version__),
    packages=("pybitturk",),
    include_package_data=True,
    keywords="bitturk turkey türkiye coin bitcoin monero btc xmr",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Software Development",
        "Typing :: Typed",
    ],
    author=pybitturk.__author__,
    author_email="eraygezer.94@gmail.com",
    license="Apache License 2.0",
    tests_require=TEST_DEPS,
    install_requires=DEPS,
    zip_safe=False,
)
