#! /usr/bin/env python

from distutils.core import setup

setup(name="nerdirc",
      version="1.0.2",
      packages=["nerdlib", 
                "nerdlib.plugins",
                "nerdlib.utils",
                "nerdlib.ircclient",
               'nerdlib.plugins.gossip', 
               'nerdlib.plugins.nickcall', 
               'nerdlib.plugins.spam', 
               'nerdlib.plugins.ajoin',
               'nerdlib.plugins.latex',
               'nerdlib.plugins.highligh',
               'nerdlib.plugins.link', 'nerdlib.plugins.jump',
               'nerdlib.plugins.nickclick'],
      scripts=['nerdirc'],
      package_data={'nerdlib': ['icon/*.gif', '*.txt', 'ircclient/*.txt', '*.cfg']},
      author="Iury O. G. Figueiredo",
      author_email="ioliveira@id.uff.br")






























