from distutils.core import setup

with open("PYPI_README.md")as readme:
    long_desc = readme.read()

setup(
    name="custos-logger",
    packages=["custos"],
    version="1.0.5",
    license="MIT",

    description="A customisable console logging package with colours and much more!",
    long_description=long_desc,

    author="Mila Software Group",
    author_email="jack@mila-software.group",

    url="https://github.com/milasoftwaregroup/custos",
    download_url="https://github.com/milasoftwaregroup/custos/archive/v1.0.0.tar.gz",

    keywords=["Logging", "Termcolor", "Ayana/logger", "Console", "Custom"],

    install_requires=["termcolor"],
    classifiers=[
        # Either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ]
)