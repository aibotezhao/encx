# -*- coding: utf-8 -*-
from __future__ import absolute_import
from setuptools import setup, find_packages

setup(
    name="encx",
    version="0.1.0-py27",
    description="CLI toolkit for common encodings (base64, hex, rot13, url) and XOR (Python 2.7 compatible).",
    author="EncX Maintainers",
    license="MIT",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "encx=encx.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Topic :: Security :: Cryptography",
        "Topic :: Utilities"
    ],
)
