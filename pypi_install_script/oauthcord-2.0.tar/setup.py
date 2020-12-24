from setuptools import setup, find_packages

with open("README.md", "r") as ld:
    long_description = ld.read()
    
setup(
    name="oauthcord",
    version="2.0",
    author="Logan Webb",
    author_email="lganWebb04@gmail.com",
    description="An Oauth2 wrapper for discord",
    long_description=long_description,
    url="https://github.com/lganWebb/oauthcord",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
