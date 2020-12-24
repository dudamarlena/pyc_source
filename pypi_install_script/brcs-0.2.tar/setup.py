import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="brcs",
    version="0.2",
    author="Yushi Yang",
    description="Biased random colors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yangyushi/brcs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy', 'matplotlib'],
    python_requires='>=2.7',
)
