#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

def readme():
    with open('README.md') as readme_file:
        return readme_file.read()

setup(
    name = '',
    version = '1.10',
    description = '',
    long_description=readme(),
    download_url = '',
    url = '',
    author = '',
    author_email = '',
    packages = ['draw_my_map'],
    license = "MIT",
    install_requires = ['Pillow'],
    entry_points='''
        [console_scripts]
        draw_my_map = draw_my_map.draw_my_map:main
    ''',
    )
