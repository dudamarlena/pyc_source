from setuptools import find_packages, setup

with open("README.rst", encoding="utf-8") as f:
    readme = f.read()


setup(
    name="dnspod-sdk",
    version="0.0.2",
    description="A dnspod api SDK",
    long_description=readme,
    classifiers=["Programming Language :: Python :: 3"],
    author="codeif",
    author_email="me@codeif.com",
    url="https://github.com/codeif/dnspod-sdk",
    keywords=["DNSPod", "DNS", "SDK"],
    license="MIT License",
    packages=find_packages(),
    install_requires=["requests"],
)
