from setuptools import find_packages, setup


with open("README.rst", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="aiohttp-bam",
    version="0.0.2",
    url="https://github.com/codeif/aiohttp-bam",
    description="aiohttp basic auth middleware.",
    long_description=readme,
    author="codeif",
    author_email="me@codeif.com",
    license="MIT",
    classifiers=["Programming Language :: Python :: 3"],
    packages=find_packages(),
)
