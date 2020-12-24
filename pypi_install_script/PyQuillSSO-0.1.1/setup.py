from setuptools import setup

setup(
    name="PyQuillSSO",
    version="0.1.1",
    packages=["pyquillsso"],
    install_requires=["requests>=2.13.0", "PyJWT>=1.4.2"],
    license="MIT",
    long_description=open("README.md").read(),
)
