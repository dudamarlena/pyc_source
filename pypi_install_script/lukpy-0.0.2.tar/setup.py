import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="lukpy", #
    version="0.0.2",
    author="Lukas Hecker",
    author_email="lukas_hecker@web.com",
    description="My personal functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/LukeTheHecker/lukpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['scipy', 'numpy', 'matplotlib']
)