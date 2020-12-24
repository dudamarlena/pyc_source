import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vortext",
    version="0.0.1",
    author="PROgramJEDI",
    author_email="tamirglobus@gmail.com",
    description="🌀 Vortext is a small library allows the machine to solve Movement and Production problems using NLP toolkits",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PROgramJEDI/vortext",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)