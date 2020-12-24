import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()


setuptools.setup(
    name="AyanREngineSDK",
    version="0.0.14",
    author="rams3sh",
    description="Python SDK for developing AyanR Engines",
    packages=["AyanREngineSDK"],
    install_requires=required,
    python_requires='>=3.6',
)
