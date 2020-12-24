from setuptools import setup, find_packages


setup(
    name="avilabs-torchutils",
    version="2.0.8",
    description="Convenience utils for using pytorch",
    author="Avilay Parekh",
    author_email="avilay@gmail.com",
    license="MIT",
    url="https://gitlab.com/avilay/torchutils",
    packages=find_packages(),
    install_requires=["torch", "torchvision", "numpy", "ax-platform", "mlflow", "haikunator"],
)
