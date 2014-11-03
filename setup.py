# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='miya-bot',
      version='0.0.4',
      description='a twitter bot inspired by amagami',
      author='choro3',
      author_email='mail@choro3.net',
      url='http://www.choro3.net/',
      packages=find_packages(),
      entry_points="""
      [console_scripts]
      miyabot = miya.main:console_script
      """)

