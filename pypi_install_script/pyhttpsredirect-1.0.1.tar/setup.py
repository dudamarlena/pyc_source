from setuptools import setup


VERSION = "1.0.1"


setup(
    name="pyhttpsredirect",
    version=VERSION,
    author="Steve McMaster",
    author_email="mcmaster@hurricanelabs.com",
    py_modules=["pyhttpsredirect"],
    description="A simple http server that forcefully redirects to https.",
    entry_points={
        "console_scripts": [
            "pyhttpsredirect = pyhttpsredirect:main",
        ]
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
    ],
    bugtrack_url="https://github.com/HurricaneLabs/pyhttpsredirect/issues",
)
