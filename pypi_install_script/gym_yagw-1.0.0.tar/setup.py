from setuptools import setup

setup(name='gym_yagw',
      version='1.0.0',
      install_requires=['gym', 'pyglet', 'numpy'],
      author='Kim Hammar',
      author_email='hammar.kim@gmail.com',
      description='YAGW - Yet Another Grid World',
      license='MIT License',
      keywords='Gridworld, reinforcement learning, Q-learning',
      url='https://github.com/Limmen/gym-yagw',
      download_url='https://github.com/Limmen/gym-yagw/archive/1.0.0.tar.gz',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6'
  ]
)
