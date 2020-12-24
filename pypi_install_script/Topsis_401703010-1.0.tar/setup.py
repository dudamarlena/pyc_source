from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="Topsis_401703010",
    version="1.0",
    description="A Python package to implement Topsis ",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Jiya Midha",
    author_email="midhajiya@gmail.com",
    license="MIT",
    url = 'https://github.com/midhajiya',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["Topsis_401703010"],
    include_package_data=True,
    install_requires=["numpy", "pandas"],
    entry_points={
        "console_scripts": [
            "Topsis_401703010=topsis.cli:main",
        ]
    },
)
