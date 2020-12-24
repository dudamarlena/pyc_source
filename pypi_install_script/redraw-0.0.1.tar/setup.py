from setuptools import setup

with open("requirements.txt", encoding="utf-8") as f:
    REQUIRED = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

with open("VERSION", "r", encoding="utf-8") as fh:
    VERSION = fh.read()
setup(
    version=VERSION,
    name="redraw",
    packages=["redraw"],
    description="An OpenSource Cloudformation Deployment Framework",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Tony Vattathil",
    author_email="tonynv@amazon.com",
    url="https://avattathil.github.io/redraw/",
    license="Apache License 2.0",
    download_url="https://github.com/avattathil/redraw/tarball/master",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Testing",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X ",
    ],
    scripts=["bin/redraw_demo"],
    keywords=["redraw"],
    install_requires=REQUIRED,
    #    test_suite="tests",
    #    tests_require=["mock", "boto3"],
    include_package_data=True,
)
