import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ssh_tunnel_boring_machine",
    version="0.1.2",
    author="Dominic Doty",
    author_email="doty.dominic@gmail.com",
    license="MIT",
    scripts=["tbm"],
    description="A tool for managing SSH tunnels from the command line",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dominicdoty/tbm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)