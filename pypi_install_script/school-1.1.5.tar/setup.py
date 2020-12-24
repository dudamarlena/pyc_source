from setuptools import setup

def readme():
    with open("README.md", "r") as f:
        README = f.read()
    return README


setup(
    name="school",
    version="1.1.5",
    description="🏫 Basic CLI for school planning.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/mortim1/school",
    author="mortim1",
    author_email="mortim1@protonmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        ],
    packages=["school"],
    include_package_data=True,
    install_requires=["bottle", "setuptools"],
    entry_points={
            "console_scripts": [
                    "school=school.school:main"
                ]
        }
)
