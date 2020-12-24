from setuptools import setup, find_packages

setup(name='nnbee',
      version='1.3',
      description='Easy Convolutional Neural Network (CNN) framework based on pytorch',
      url='https://github.com/sraashis/ature',
      download_url='https://github.com/sraashis/nnbee/releases/tag/1.3',
      author='Aashis Khanal',
      author_email='sraahis@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['numpy', 'PILLOW', 'matplotlib', 'opencv-python'],
      classifiers=[
          "Programming Language :: Python :: 3",
          'License :: OSI Approved :: MIT License',
          "Operating System :: OS Independent",
      ],
      zip_safe=True)
