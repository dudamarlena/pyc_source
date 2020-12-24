from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="topsis34",
    version="1.0.1",
    description="A Python package for topsis.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/ramneet99",
    author="Ramneet Singh",
    author_email="ramneet2511@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["topsis"],
    include_package_data=True,

    entry_points={
        "console_scripts": [
            "topsis34=topsis.entry:main",
        ]
    },
)
