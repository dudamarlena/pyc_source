import setuptools

setuptools.setup(
    name="dummy-layer-test",
    # should correlate with git tag
    version="0.5",
    author="superDross",
    author_email="dross78375@gmail.com",
    description="Lambda layer dependancy testing",
    url="https://github.com/superDross/dummy-layer-test",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
