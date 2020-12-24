import setuptools

with open("REAMDE.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Ajith_Kumar_Ravichander", # Replace with your own username
    version="0.0.1",
    author="Ajith_Kumar_Ravichander",
    author_email="ajithkumar3001@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)