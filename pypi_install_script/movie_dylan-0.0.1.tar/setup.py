from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="movie_dylan",
    version="0.0.1",
    author="Dylan",
    author_email="lidelin@netsdl.com",
    description="test pypi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://lidelin@git.netsdl.com/lidelin/Movie",
    packages=find_packages(),
    install_requires=["numpy", "opencv-python"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    keywords='Movie python'
)
