from setuptools import setup

exec(open("xirasol/version.py").read())

setup(
    name="xirasol",
    version=__version__,
    description="Placeholder for xirasol.",
    long_description="placegolder for xirasol.",
    keywords="deep reinforcement learning",
    url="https://github.com/fywu85/xirasol",
    author="Fangyu Wu",
    author_email="fangyuwu@berkeley.edu",
    license="MIT",
    install_requires=["numpy",
                      "tensorflow"]
)
