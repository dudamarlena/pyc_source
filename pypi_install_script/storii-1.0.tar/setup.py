import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="storii",
    version="1.0",
    author="Guillaume Fe",
    author_email="guillaume.ferron@gmail.com",
    description="Build little ascii friends that can speak and move",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/guillaumefe/storii",
    py_modules = ['storii'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': [
            'storii = storii:cli_storii',
            ],
        },
    python_requires='>=3.6',
)
