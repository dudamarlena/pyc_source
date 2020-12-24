import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deployx-server-sdk", # Replace with your own username
    version="1.0.1",
    author="captainkryuk",
    author_email="andrey.kryukov@protonmail.com",
    description="Package for getting feature point from DeployX app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests'
    ],
    python_requires='>=3.4',
)