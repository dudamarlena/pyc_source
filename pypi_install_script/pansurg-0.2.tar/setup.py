import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="pansurg",
    version=0.2,
    author="Maxwell Flitton",
    author_email="maxwellflitton@gmail.com",
    description="Basic pip module for accessing coronavirus resources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maxwellflitton/pansurg",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Build Tools"
    ),
    install_requires=[],
    zip_safe=False
)
