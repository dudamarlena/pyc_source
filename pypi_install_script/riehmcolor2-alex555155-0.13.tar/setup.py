import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="riehmcolor2-alex555155", # Replace with your own username
    version="0.13",
    author="Alex Riehm",
    author_email="kf5uum@gmail.com",
    description="Color analysis suite (opencv-python)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
	install_requires=['opencv-python', 'easygui', 'numpy', 'xlsxwriter', 'scikit-learn', 'tqdm']
)


#from setuptools import setup

#setup(
#    name='riehmcolor2',
#    version='2',
#    packages=['riehmcolor2'],
#    url='',
#    license='',
#    author='kf5uu',
#    author_email='kf5uum@gmail.com',
#    description='', install_requires=['opencv-python', 'easygui', 'numpy', 'xlsxwriter', 'scikit-learn', 'tqdm']
#)




