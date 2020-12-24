from setuptools import setup

import colormask

with open("README.md", "r") as f:
    README = f.read()

with open("requirements.txt", "r") as f:
    DEPS = f.readlines()

setup(
    name="colormask",
    version=colormask.__version__,
    description="colormask is a library to mask image based on colors.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/erayerdin/colormask",
    download_url="https://github.com/erayerdin/colormask/archive/master.zip",
    packages=["colormask"],
    include_package_data=True,
    keywords="python image processing mask masking logo icon",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Multimedia :: Graphics",
    ],
    author=colormask.__author__,
    author_email="eraygezer.94@gmail.com",
    license="Apache License 2.0",
    tests_require=["pytest", "coverage"],
    install_requires=DEPS,
    zip_safe=False,
)
