import setuptools
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()
setuptools.setup(name='imageserver',
      version='0.1.4',
      description='Host thumbnails for images   ',
      long_description=long_description,
      author='Nidhi Chandra',
      url='',
      author_email='chandranidhi45@gmail.com',
      license='MIT',
      zip_safe=False,
      packages=setuptools.find_packages(),
    install_requires=[
        'docopt',
        'flask',
        'pillow',
        'opencv-python'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'imageserver = imageserver.server:main',
        ],
        })
