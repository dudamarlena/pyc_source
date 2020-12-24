from setuptools import find_packages, setup

with open("README.rst", encoding="utf-8") as f:
    readme = f.read()


setup(
    name="kong-admin",
    version="0.0.2",
    description="A kong admin api sdk.",
    long_description=readme,
    author="codeif",
    author_email="me@codeif.com",
    url="https://github.com/codeif/kong-admin",
    license="MIT",
    install_requires=["requests"],
    packages=find_packages(),
)
