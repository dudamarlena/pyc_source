""" setup

"""


import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tdroid",
    package=["tdroid"],
    version="0.0.2",
    liscence="MIT",
    author="Joshua Sello",
    author_email="joshuasello@gmail.com",
    description="A python library for building robots with micro-controllers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joshuasello/tdroid",
    packages=setuptools.find_packages(),
    download_url="https://github.com/joshuasello/tdroid/archive/tdroid-v0.0.2.tar.gz",
    keywords=["raspberrypi", "microcontroller"],
    classifiers=[
        "Programming Language :: Python :: 3",
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
