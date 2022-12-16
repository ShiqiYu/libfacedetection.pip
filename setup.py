#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension
import os
__version__ = "0.0.1"

include_dirs = ['libfacedetection/include']
library_dirs = ['libfacedetection/lib']
libraries = ['facedetection']

runtime_library_dirs = [os.path.abspath(_) for _ in library_dirs]

ext_modules = [
    Pybind11Extension(
        "yudet",
        ["src/main.cpp"],
        define_macros = [('VERSION_INFO', __version__)],
        include_dirs = include_dirs,
        library_dirs = library_dirs,
        libraries = libraries,
        runtime_library_dirs = runtime_library_dirs,
        cxx_std=11,
        language='c++'
        ),
]
setup(ext_modules=ext_modules)