#!/usr/bin/env python3
"""
Setup script for Numium Compiler
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="numium-compiler",
    version="0.1.0",
    author="Numium Contributors",
    description="Numium Language Compiler - Compile to bytecode for VM execution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Khoapython-dev/numium",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'numiac=vm.compiler.numiac:main',
        ],
    },
)
