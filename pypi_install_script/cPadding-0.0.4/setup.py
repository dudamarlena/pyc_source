"""
setup
-----
"""

from setuptools import setup, find_packages
from setuptools.extension import Extension

try:
    from Cython.Build import cythonize
except ImportError:
    extensions = [Extension("cPadding", sources=["cPadding.pyx"])]
else:
    extensions = cythonize(
        "cPadding.pyx",
        compiler_directives={
            "language_level": 3,
            "cdivision": True,
            "infer_types": True,
            "overflowcheck": True,
        }
    )


setup(
    name="cPadding",
    description="Padding methods for password based encryption implemented in Cython",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/initbar/cPadding",
    author="Herbert Shin",
    author_email="h@init.bar",
    version="0.0.4",
    license="MIT",
    setup_requires=[
        "cython>=0.29.4",
    ],
    python_requires=">=2.7",
    packages=find_packages(exclude=["tests"]),
    ext_modules=extensions,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],
)
