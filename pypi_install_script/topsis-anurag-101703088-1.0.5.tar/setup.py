from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="topsis-anurag-101703088",
    version="1.0.5",
    description="A Python package to choose the best alternative from a finite set of decision alternatives.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url = 'https://github.com/user/101703088-topsis',
    download_url="https://github.com/Anurag-Aggarwal/101703088-topsis/blob/master/topsis.py",
    author="Anurag Aggarwal",
    author_email="agrawalanurag321@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["topsis"],
    include_package_data=True,
    install_requires=["os","pandas","math","numpy"],
    entry_points={
        "console_scripts": [
            "topsis-101703088=topsis.topsis:main",
        ]
    },
) 