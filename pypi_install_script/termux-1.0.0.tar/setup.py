from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="termux",
    version="1.0.0",
    description="A Python based Termux api wrapper",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/AXDZ/termux",
    author="Aldas",
    author_email=None,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["termux"],
    include_package_data=True,
    install_requires=None,
    entry_points={
        "console_scripts": [
            "termux=api:main",
        ]
    },
)
