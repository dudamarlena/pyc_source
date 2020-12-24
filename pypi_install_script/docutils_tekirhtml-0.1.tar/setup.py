from setuptools import setup, find_packages


with open("README.rst") as readme_file:
    readme = readme_file.read()


setup(
    name="docutils_tekirhtml",
    version="0.1",
    description="Custom HTML writer for docutils.",
    long_description=readme,
    author="H. Turgut Uyar",
    author_email="uyar@tekir.org",
    license="BSD",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Documentation",
        "Topic :: Utilities",
    ],
    platforms="any",
    py_modules=["tekirhtml"],
    install_requires=["docutils>=0.14"],
)
