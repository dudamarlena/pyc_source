import setuptools

exec(open("mattermost/version.py").read())

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mattermost",
    version=__version__,
    author="someone",
    author_email="someone@somenet.org",
    description="Mattermost API bindings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://git.somenet.org/pub/jan/mattermost_api.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests", "websockets",
    ],
)
