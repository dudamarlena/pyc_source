from setuptools import setup




with open("README.md", "r") as fh:
    long_description = fh.read()




setup(name='pdf_mail',
      version='3.0.0',
      author="vasu_gupta",
      description='Sending pdf document through gmail using python ',
      long_description=long_description,
      url="https://github.com/vasu04gupta/Sending-Email",
      packages=['pdf_mail'],classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],zip_safe=False)


