import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="citcall-py",
    version="0.1.1",
    author="Saggaf Arsyad",
    author_email="saggaf@nbs.co.id",
    description="Citcall REST API for Python",
    license="MIT",
    long_description="Provide Citcall function for Sync/Async Miscall, SMS and SMS OTP. Forked from citcall-devel",
    long_description_content_type="text/markdown",
    url="https://github.com/saggafarsyad/citcall-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
