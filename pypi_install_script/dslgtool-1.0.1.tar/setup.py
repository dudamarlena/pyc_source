from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = 'dslgtool',
    version = '1.0.1',
    author = 'longlamduc',
    description = 'A tool to detect image location',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    packages = find_packages(),
    install_requires=[
        'requests',
        'cryptography',
        'exifread',
        'pillow',
        'gpsphoto',
        'piexif',
        'opencv-python',
      ],
    entry_points = {
        'console_scripts': [
            'dslgtool = dslgtool.__main__:main'
        ]
    },
    python_requires='>=3.6',
    )