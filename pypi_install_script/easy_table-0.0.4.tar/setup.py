import setuptools

with open("README.md", "r") as file:
    readme = file.read()

setuptools.setup(
    name="easy_table",
    packages=["easy_table"],
    version="0.0.4",
    author="Jacob Rumbolt",
    author_email="rumboltjacob@gmail.com",
    description="An easy to use python module for creating, editing, and displaying tables",
    long_description = readme,
    long_description_content_type = "text/markdown",
    url="https://github.com/TheGuyFromCanada/Easy-Table",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ]
)
