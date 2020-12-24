from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="topsis-daman",
    version="1.0.0",
    description="A Python package to implement Topsis analysis",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Damanpreet Singh",
    author_email="preetdamansingh1998@gmail.com",
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
            "topsis-daman=topsis.cli:main",
        ]
    },
)