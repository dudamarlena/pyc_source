import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# See https://packaging.python.org/tutorials/packaging-projects/
setuptools.setup(
    name="logolas",
    version="0.0.1",
    description="Analysis and summarization tool for logs and traces of the Elrond Node",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ElrondNetwork/logolas",
    author="Elrond Network",
    license="GPL",
    packages=setuptools.find_packages(
        include=["logolas*"], exclude=[]),
    include_package_data=True,
    install_requires=[
        "texttable"
    ],
    zip_safe=False,
    keywords=["Elrond"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha"
    ],
    entry_points={
        "console_scripts": [
            "logolas=logolas.cli:main",
        ],
    },
    python_requires=">=3.6"
)
