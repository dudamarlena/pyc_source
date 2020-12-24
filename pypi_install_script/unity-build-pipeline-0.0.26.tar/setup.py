import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="unity-build-pipeline",
    version="0.0.26",
    author="Vitaliy Krasnoperov",
    author_email="alistar.neron@gmail.com",
    description="Unity build pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neronmoon/UnityBuildPipeline",
    packages=setuptools.find_packages(),
    install_requires=required,
    scripts=['pipeline'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
