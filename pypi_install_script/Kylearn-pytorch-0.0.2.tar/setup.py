import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Kylearn-pytorch", # Replace with your own username
    version="0.0.2",
    author="Jincheng Sun",
    author_email="sjc951213@gmail.com",
    description="A deep learning package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jincheng-Sun/Kylearn-pytorch",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)