import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cs200",
    version="2.4.5",
    packages=["cs200"],
    author="Joshua Segal",
    author_email="gitpulljoshuasegal@gmail.com",
    description="A SIMPLE package for simplifying concepts available on wikipedia.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dev-segal/cs200",
    install_requires = [
        "flask",
        "summa",
        "bs4"
        ],
        entry_points = {
    'console_scripts' : ["cs200=cs200.bin:main", "cs200-install=cs200.bin:install"],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)
