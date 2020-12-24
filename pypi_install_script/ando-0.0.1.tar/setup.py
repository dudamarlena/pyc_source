from setuptools import setup, find_packages

setup(
    name="ando",
    version="0.0.1",
    packages=find_packages(exclude=["tests*"]),
    license="MIT",
    description="Manipulate, scrape, and analyze visual media",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[],
    url="https://github.com/concurrent-studio/ando",
    author="concurrent-studio",
    author_email="info@concurrent.studio",
    package_data={
        "ando": ["ando/models/*.(mat|pb|xml)"]
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research"
    ]
)
