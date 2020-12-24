from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="certbot_anx",
    version="0.1",
    description="ANX DNS authentication plugin for Certbot",
    license="BSD",
    author="Marky Egebäck",
    author_email="marky@egeback.se",
    url="https://github.com/egeback/pycertbot-anx",
    py_modules=["certbot_anx"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "certbot>=0.37.0",
        "pyanxdns>=0.2",
        "zope.interface>=4.4.0"
    ],
    entry_points={
        "certbot.plugins": [
            "auth = certbot_anx:ANXAuthenticator",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: Name Service (DNS)",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
)