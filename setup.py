#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

def readme():
    with open('README.md') as readme_file:
        return readme_file.read()

setup(
    name = 'draw_my_map',
    version = '1.0.1',
    description = 'draw_my_map',
    long_description=readme(),
    download_url = 'https://github.com/dellielo/draw-my-map',
    url = 'https://github.com/dellielo/draw-my-map',
    author = 'Elodie Dellier',
    author_email = 'dellier.elodie@gmail.com',
    packages = ['draw_my_map'],
    license = "MIT",
    install_requires = [],
    classifiers = [
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.4',
        ],
    entry_points='''
        [console_scripts]
        
    ''',
    )