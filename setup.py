#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.build_ext import build_ext
from setuptools.command.install import install
from pybind11.setup_helpers import Pybind11Extension
import os
import platform
import sys
import shutil


__version__ = "0.0.1"

dbr_lib_dir = ''
dbr_include = ''
dbr_lib_name = 'libfacedetection'

# linux
if sys.platform == "linux" or sys.platform == "linux2":
    if platform.uname()[4] == 'AMD64' or platform.uname()[4] == 'x86_64':
            dbr_lib_dir = 'lib/linux'
    elif platform.uname()[4] == 'aarch64':
            dbr_lib_dir = 'lib/aarch64'
    else:
            dbr_lib_dir = 'lib/arm32'
    ext_args = dict(        
        include_dirs=['include'],
        libraries = [dbr_lib_name],
        library_dirs = [dbr_lib_dir],
        extra_compile_args = ['-std=c++11'],
        extra_link_args = ["-Wl,-rpath=$ORIGIN"],
        define_macros = [('VERSION_INFO', __version__)],
        language='c++',
        cxx_std=11,
    )
# windows
elif sys.platform == "win32":
    dbr_lib_name = 'DBRx64'
    dbr_lib_dir = 'lib/win'
    ext_args = dict(
        include_dirs=['include'], 
        libraries=[dbr_lib_name],
        library_dirs = [dbr_lib_dir],
        define_macros = [('VERSION_INFO', __version__)],
        language='c++',
        cxx_std=11,
    )
        
yudet_modules = [
    Pybind11Extension(
        "yudet",
        ["src/main.cpp"],
        **ext_args
        ),
]

def copylibs(src, dst):
    if os.path.isdir(src):
        filelist = os.listdir(src)
        for file in filelist:
                libpath = os.path.join(src, file)
                shutil.copy2(libpath, dst)
    else:
        shutil.copy2(src, dst)

class CustomBuildExt(build_ext):
    def run(self):
        build_ext.run(self)
        dst =  os.path.join(self.build_lib, "barcodeQrSDK")
        copylibs(dbr_lib_dir, dst)
        filelist = os.listdir(self.build_lib)
        for file in filelist:
            filePath = os.path.join(self.build_lib, file)
            if not os.path.isdir(file):
                copylibs(filePath, dst)
                # delete file for wheel package
                os.remove(filePath)

class CustomBuildExtDev(build_ext):
    def run(self):
        build_ext.run(self)
        dev_folder = os.path.join(os.path.dirname(__file__), 'barcodeQrSDK')
        copylibs(dbr_lib_dir, dev_folder)
        filelist = os.listdir(self.build_lib)
        for file in filelist:
            filePath = os.path.join(self.build_lib, file)
            if not os.path.isdir(file):
                copylibs(filePath, dev_folder)

class CustomInstall(install):
    def run(self):
        install.run(self)

setup(ext_modules=yudet_modules, 
      cmdclass={'build_ext': CustomBuildExt, 'install': CustomInstall, 'develop': CustomBuildExtDev})