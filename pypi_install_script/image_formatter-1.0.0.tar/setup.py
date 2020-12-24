import setuptools


setuptools.setup(name='image_formatter',
      version="1.0.0",
      url = "https://github.com/stkobsar/image_formatter", 
      description='Transform image .ORF to jpg and more!',
      author='Stephi Kobsar',
      author_email='stkobsar7@gmail.com',
      packages=setuptools.find_packages(),
      install_requires=["Pillow", "rawpy", "imageio"],
      classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
       ],
     )
