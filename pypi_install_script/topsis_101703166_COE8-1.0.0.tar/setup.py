from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="topsis_101703166_COE8",
    version="1.0.0",
    description="A Python package to implement Topsis analysis",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="dhriti",
    author_email="djindal612@gmail.com",
    license="MIT",
    url = 'https://github.com/DhritiJindal27/Topsis-Dhriti',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["topsis_101703166_COE8"],
    include_package_data=True,
    install_requires=["numpy", "pandas"],
    
)
