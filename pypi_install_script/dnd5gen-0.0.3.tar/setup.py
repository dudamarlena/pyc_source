from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="dnd5gen",
    version="0.0.3",
    author="Valkyrie",
    author_email="valkyrie@r3valkyrie.com",
    description="Library to help implement random 5e character generation into my projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/r3valkyrie/dnd5gen",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
    include_package_data=True
)
