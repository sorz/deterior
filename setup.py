#!/usr/bin/env python3
from setuptools import setup

from deterior import __version__ as version


setup(
    name='deterior',
    version=version,
    description='Equipment Deterioration Modeling Tools',
    packages=['deterior'],
    entry_points="""
    [console_scripts]
    deterior = deterior:run
    """,
    python_requires='>=3.6',
    install_requires=[
        'numpy',
    ]
)
