# -*- coding: utf-8 -*-
"""
Author: zero
Email: 13256937698@163.com
Date: 2019-11-06
"""
from __future__ import print_function
from setuptools import setup, find_packages


with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="thctools",
    version="1.0.1",
    author="zero",
    author_email="13256937698@163.com",
    description="Used as an indicator to study the trend of the stock market. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/zero-python/thctools",
    packages=find_packages(),
    install_requires=[

        ],

    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',

    ],

)
