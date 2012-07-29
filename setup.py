#!/usr/bin/env python

from distutils.core import setup

setup(name='ADBGen',
    version='1.0',
    description='Android Database Generator',
    author='Sutee Sudprasert',
    author_email='sutee.s@gmail.com',
    scripts=['adbgen_run'],
    packages=['adbgen'],
)