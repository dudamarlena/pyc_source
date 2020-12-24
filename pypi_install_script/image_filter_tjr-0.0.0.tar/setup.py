# TODO: Fill out this file with information about your package

# HINT: Go back to the object-oriented programming lesson "Putting Code on PyPi" and "Exercise: Upload to PyPi"

# HINT: Here is an example of a setup.py file
# https://packaging.python.org/tutorials/packaging-projects/

import setuptools

setuptools.setup(
    name='image_filter_tjr',
    description='Simple and Auto Thresholding of Images',
    packages=setuptools.find_packages(),
    zip_safe=False
)