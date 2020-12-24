from setuptools import find_packages, setup

setup(
    author = "youmeng",
    license = "MIT",
    name = "youmeng",
    version = "1.0.0",
    url = "https://developer.umeng.com/open-api/docs/com.umeng.uapp/umeng.uapp.getAllAppData/1#!!open-api-doc-tools",
    install_requires = [],
    py_modules = ["test"],
    packages = find_packages(),
    long_description = open("README.md").read(),
    long_description_content_type='text/markdown',
    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: POSIX",
    ]
)
