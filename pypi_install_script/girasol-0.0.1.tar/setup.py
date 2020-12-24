from setuptools import setup

exec(open("girasol/version.py").read())

setup(
    name="girasol",
    version=__version__,
    description="Placeholder for girasol.",
    long_description="placegolder for girasol.",
    keywords="deep reinforcement learning",
    url="https://github.com/fywu85/girasol",
    author="Fangyu Wu",
    author_email="fangyuwu@berkeley.edu",
    license="MIT",
    install_requires=["numpy",
                      "tensorflow"]
)
