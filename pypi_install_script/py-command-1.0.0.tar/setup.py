from setuptools import find_packages, setup

with open("README.rst", "r") as fh:
    long_description = fh.read()


setup(
    name="py-command",
    author="SnoopyBoy",
    author_email="785576549@qq.com",
    packages=find_packages(),
    version="1.0.0",
    description="A small tool for python command and sub command.",
    license='MIT',
    long_description=long_description,
    url="https://github.com/zhd785576549/py-command",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ]
)
