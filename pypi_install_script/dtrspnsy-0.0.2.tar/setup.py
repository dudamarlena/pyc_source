import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dtrspnsy",
    version="0.0.2",
    author="upgradehq",
    author_email="noreply@example.com",
    description="search dota 2 responses english/russian/chinese",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dota2tools/dtrspnsy",
    packages=["dtrspnsy"],
    install_requires=['prompt_toolkit'],
    package_data={
        "dtrspnsy": ["en_replics/*.json", "ru_replics/*.json", "zh_replics/*.json"]
    },
    entry_points={"console_scripts": ["dtrspnsy=dtrspnsy.dtrspnsy:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # for pathlib and f strings
    python_requires=">=3.6",
)
