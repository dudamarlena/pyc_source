import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()


setuptools.setup(
    name="ayanRAgent",
    version="0.0.13",
    author="rams3sh",
    description="ayanR Agent to manage all the jobs assigned by ayanR Manager",
    packages=["ayanRAgent"],
    scripts=["ayanRAgent/ayanRAgent.py"],
    install_requires=required,
    python_requires='>=3.6',
)
