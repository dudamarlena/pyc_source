from setuptools import setup

setup(name='modellogger',
      version='0.1.2',
      url='https://github.com/SohamPathak/modellogger',
      author='SohamPathak',
      author_email='sohamkiit636@gmail.com',
      license='None',
      packages=['modellogger'],
      zip_safe=False,
	#license="LICENSE.txt",
	description="Tool for model performance monitoring | First Iteration 3/29/2020",
      #long_description=open("README.txt").read(),
	  install_requires=[
		"flask",
		"pandas",
		"numpy",
		"sklearn"
		],





      )