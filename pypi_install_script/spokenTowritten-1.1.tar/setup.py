from setuptools import setup

with open("README.md", 'r') as f:
  long_description_ = f.read()


setup(
    name='spokenTowritten',
    packages=['spokenTowritten'],
    version='1.1',
    license='MIT',        # https://help.github.com/articles/licensing-a-repository
    description="Library For Spoken to written",   # Give a short description about your library
    long_description=long_description_,
    long_description_content_type='text/markdown',
    author='Raman Shinde',
    author_email='raman.shinde15@gmail.com',
    url='https://github.com/Raman-Raje/spokenTowritten',   # Provide either the link to your github or to your website
    download_url='https://github.com/Raman-Raje/spokenTowritten/archive/v_1.1.tar.gz',
    install_requires=[
        'forex-python',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
