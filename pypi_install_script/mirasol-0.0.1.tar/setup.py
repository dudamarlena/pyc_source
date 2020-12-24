from setuptools import setup

exec(open("mirasol/version.py").read())

setup(
    name="mirasol",
    version=__version__,
    description="A self-contained backend-independent version of FLOW for (deep) reinforcement learning in a network environment.",
    long_description="This is a minimized version of FLOW (https://github.com/berkeleyflow/flow) stack. It allows users to define a custom environment backend and a custom agent backend. The current version supports SUMO (https://github.com/eclipse/sumo) as the environment backend and tensorflow (https://github.com/tensorflow) as the agent backend.",
    keywords="deep reinforcement learning on networks",
    url="https://github.com/fywu85/mirasol",
    author="Fangyu Wu",
    author_email="fangyuwu@berkeley.edu",
    license="MIT",
    install_requires=["numpy",
                      "tensorflow"]
)
