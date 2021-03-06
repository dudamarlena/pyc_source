from setuptools import setup,find_packages



setup(name='wm_ssim',
      version='0.2.2',
      description='The library to find WM_SSIM of a webapge with all the transformations',
      packages = ['wm_ssim'],
      url='http://github.com/abdul-manaan/wm_ssim',
      author='Abdul Manan',
      author_email='manan.lums@gmail.com',
      license='MIT',
      install_requires=[
            'selenium==3.141.0',
            'numpy==1.11.0',
            'opencv_python==4.1.1.26',
            'scikit_image',
            'matplotlib',
            'Pillow==6.1.0',
            'beautifulsoup4==4.8.0',
            'python_magic==0.4.15',
            'pyvirtualdisplay==0.2.4'],
      zip_safe=False,
      classifiers=[
        'Programming Language :: Python :: 2'
      ])