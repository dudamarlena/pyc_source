from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="topsis-hiten",
    version="2.0.0",
    description="A Python package to implement Topsis analysis",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/hitengarg45/topsis-hiten-101703234",
    author="Hiten Garg",
    author_email="hitengarg20@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["topsis"],
    include_package_data=True,
    install_requires=["numpy", "pandas"],
    entry_points={
        "console_scripts": [
            "topsis-hiten=topsis.cli:main",
        ]
    },
)