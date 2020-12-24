import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shameless",
    version="0.0.2",
    author="Seyoung Song",
    author_email="seyoung@macbook.local",
    description="Shameless browser automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seyoungsong/shameless",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'beautifulsoup4',
        'bs4',
        'selenium',
        'tqdm',
        'requests',
    ],
)
