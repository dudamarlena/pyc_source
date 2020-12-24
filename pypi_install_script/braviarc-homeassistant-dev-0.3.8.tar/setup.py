import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="braviarc-homeassistant-dev", # Replace with your own username
    version="0.3.8",
    maintainer="David Nielsen",
    maintainer_email="dncielsen90@gmail.com",
    description="bravia tv controller for home-assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dcnielsen90/braviarc.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
