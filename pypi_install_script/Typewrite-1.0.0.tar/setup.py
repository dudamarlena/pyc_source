 
import setuptools 
with open("README.md", "r") as fh:
    long_description = fh.read() 
#The current directory

setuptools.setup(
    name="Typewrite",
    version="1.0.0",
    author="Rhett Henderson",
    author_email="rhett.henderson@outlook.com",
    description="A package to allow for more print functinality.",
    long_description=long_description,
    lomg_description_content_type="text/markdown",
    url="https://github.com/WorkingCupid549/Typewrite", #Add my Gihub later
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3", 
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX"
    ],
)