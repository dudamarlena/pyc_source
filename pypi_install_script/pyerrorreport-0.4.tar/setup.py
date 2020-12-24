from setuptools import setup

setup(name='pyerrorreport',
      version='0.4',
      description='Send error reports and other messages to a central server you control.',
      url='https://gitlab.com/toastengineer/pyerrorreport',
      author='TOASTEngineer',
      author_email='toastengineer@gmail.com',
      license='MIT',
      packages=['pyerrorreport'],
      zip_safe=False,
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ]
      )