import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='accipio',
                 version='0.2',
                 description='TensorFlow made easy!',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 keywords='AI',
                 author='Anders Matre',
                 author_email='andersmatre2001@gmail.com',
                 packages=setuptools.find_packages(),
                 license='Apache License 2.0',
                 zip_save=False,
                 classifiers=[
                     'Development Status :: 3 - Alpha',
                     'Programming Language :: Python :: 3.6',
                     'License :: OSI Approved :: Apache Software License',
                     'Operating System :: OS Independent',
                 ],
                 python_requires='>=3.6',
                 install_requires=[
                     'tensorflow',
                     'beautifulsoup4',
                     'matplotlib',
                     'numpy',
                     'Pillow',
                 ],
                 )
