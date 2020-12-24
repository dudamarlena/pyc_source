import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="darwin_pytorch",
    version="0.1.2",
    author="Rickard Sjoegren",
    author_email="rickard.sjoegren@sartorius.com",
    description="Small package for interfacing V7Lab's Darwin with Pytorch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sartorius-research/darwin-pytorch",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    python_requires='>=3.6',
    install_requires=[
        'darwin @ git+https://github.com/v7labs/darwin-cli@7cb9fb3d2259aac3493c1b886d57223af737b0f0',
        'numpy'
    ]
)