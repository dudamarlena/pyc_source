import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sgftree",  # Replace with your own username
    version="0.0.4",
    author="Oleksandr Hiliazov",
    author_email="oleksandr.hiliazov@gmail.com",
    description="A package to work with SGF files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment :: Board Games",
    ],
    python_requires='>=3.7',
)
