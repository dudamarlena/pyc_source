import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lcommit.hook",
    version="1.0.5",
    author="Paul Rosset",
    author_email="paulrosset96@gmail.com",
    description="Reproduce the github webhook when commit.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PaulRosset/lcommit-hook",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    entry_points={
        "console_scripts": [
            'lcommit = hook:main',
        ],
    }
)
