from setuptools import setup

setup(
    name="goarch_api",
    version="1.1.1",
    author="Elliott Pardee",
    author_email="me@vypr.xyz",
    url="https://github.com/Oikonomia/goarch_api",
    license="GPLv3",
    packages=["goarch_api"],
    description="A Python interface for the Greek Orthodox Archdiocese of America's Chapel API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=["lxml", "requests"],
    python_requires=">=3.6.5",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Religion",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Natural Language :: Greek",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet",
        "Topic :: Religion",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ]
)