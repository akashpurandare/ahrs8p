#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

readme = open("README.md", "r").read()

import ahrs8p
version = ahrs8p.__version__

setup(
    name="ahs8p",
    version=version,
    description="ASV ahrs8p",
    long_description=readme,
    long_description_content_type='text/markdown',
    author="Akash Purandare",
    author_email="akash.p1997@gmail.com",
    url="https://github.com/akashp1997/asvprotobuf",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[],
    license="BSD-3-Clause",
    zip_safe=True,
    keywords="ahrs8p",
)