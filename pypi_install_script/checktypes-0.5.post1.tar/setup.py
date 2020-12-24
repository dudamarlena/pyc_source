from setuptools import setup


package_name = "checktypes"
version = "0.5.post1"
url = "https://gitlab.com/yahya-abou-imran/checktypes"
description = (
    "Library for creating utility classes giving a nice "
    "abstraction for type checking and data validation"
)


with open("README.md") as f:
    long_description = f.read()


setup(
    name=package_name,
    description=description,
    long_description_content_type='text/markdown',
    long_description=long_description,
    version=version,
    author="Yahya Abou Imran",
    author_email="yahya-abou-imran@protonmail.com",
    license="GPLv3",
    url=url,
    packages=[package_name],
    python_requires=">=2.7",
    install_requires=[
        "six",
    ],
)
