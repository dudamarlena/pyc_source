import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="7i96",
    version="0.0.2",
    author="John Thornton",
    author_email="bjt128@gmail.com",
    description="LinuxCNC 2.8 Mesa 7i96 Configuration Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jethornton/7i96",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ),
)
