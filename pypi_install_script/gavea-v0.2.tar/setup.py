from distutils.core import setup

setup(
    name="gavea",
    packages=["gavea"],
    version="v0.2",
    license="MIT",
    description="A modern state-space framework",
    author="Mario Souto",
    author_email="mariohsouto@gmail.com",
    url="https://github.com/mariohsouto",
    download_url="https://github.com/mariohsouto/gavea/archive/v0.2.tar.gz",
    keywords=["state-space", "control-theory", "filtering"],
    install_requires=["cvxpy", "matplotlib",],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
