import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pconfig",
    version="0.0.2",
    author="John Thornton",
    author_email="bjt128@gmail.com",
    description="LinuxCNC 2.8 Parallel Port Configuration Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jethornton/pconfig",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ),
)
