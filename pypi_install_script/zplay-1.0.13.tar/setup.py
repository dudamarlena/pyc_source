from setuptools import setup, find_packages

setup(
    name="zplay",
    version='1.0.13',
    zip_safe=False,
    platforms='any',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    install_requires=['setproctitle', 'netkit', 'pyglet'],
    url="https://github.com/dantezhu/zplay",
    license="MIT",
    author="dantezhu",
    author_email="zny2008@gmail.com",
    description="zplay",
)
