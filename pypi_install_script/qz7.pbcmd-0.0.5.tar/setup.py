from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

    lines = long_description.strip()
    lines = lines.split("\n")
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line]

    package_name = lines[0].lstrip("#").strip()
    print("package_name:", package_name)

    description = lines[1]
    print("description:", description)

setup(
    name=package_name,
    description=description,

    author="Parantapa Bhattacharya",
    author_email="pb+pypi@parantapa.net",

    long_description=long_description,
    long_description_content_type="text/markdown",

    packages=[package_name],
    scripts=["bin/pb"],

    use_scm_version=True,
    setup_requires=['setuptools_scm'],

    install_requires=[
        "click",
        "click_completion",
        "logbook",
        "toml",
        "python-dateutil",
        "qz7.shell"
    ],

    url="http://github.com/parantapa/%s" % package_name,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
