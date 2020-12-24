import setuptools


with open("README.md", "rb") as fh:
    long_description = fh.read().decode()


setuptools.setup(
    name="logging-reset",
    version="10.0.3",
    author="Maybe Null",
    author_email="maybenull@protonmail.ch",
    description="Reset Python logging configuration to factory defaults",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
)

