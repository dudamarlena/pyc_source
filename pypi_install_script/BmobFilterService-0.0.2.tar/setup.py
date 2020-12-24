import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BmobFilterService",
    version="0.0.2",
    author="ketu",
    author_email="302692949@qq.com",
    description="OneCubeSpider Filter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/llketu",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)