import setuptools


setuptools.setup(name='word_polysemy',
      version="1.0.0",
      url = "https://github.com/cristinafareizaga/word_polysemy.git",
      description='Get the polysemy of each word',
      author='Cristina Areizaga',
      author_email='cristinafareizaga@gmail.com',
      packages=setuptools.find_packages(),
      install_requires=['matplotlib','pandas','bs4','requests'],
      classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License"
       ],
     )