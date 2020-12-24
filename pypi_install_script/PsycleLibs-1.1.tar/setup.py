from setuptools import setup

setup(name='PsycleLibs',
      version='1.1',
      author="Arunava Maulik",
      description="Private Repository for Psycle Research",
      url="https://github.com/PsycleResearch/PsycleLibs",
      packages=['PsycleLibs'],
      install_requires=["numpy", "torch >= 1.4", "opencv-python", "torchvision"],
      python_requires='>=3.6'
      )
