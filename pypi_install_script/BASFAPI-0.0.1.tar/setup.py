import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BASFAPI", # Replace with your own username
    version="0.0.1",
    author="Pablo Ruiz",
    author_email="pablo.ruiz@basf.com",
    description="APIs for the future",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requieres = [
        'numpy',
        'pandas'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)