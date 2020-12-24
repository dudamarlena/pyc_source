import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zerolibs",
    version="0.0.1",
    author="ZeroWangZY",
    author_email="756762961@qq.com",
    description="a libs for myself",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZeroWangZY/zerolib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)