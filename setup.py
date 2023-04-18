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

lib_name = 'facedetection'
lib_dir = ''

# linux
if sys.platform == "linux" or sys.platform == "linux2":
    if platform.uname()[4] == 'AMD64' or platform.uname()[4] == 'x86_64':
            lib_dir = 'lib/linux/x64/avx2'
    elif platform.uname()[4] == 'aarch64':
            lib_dir = 'lib/linux/aarch64/avx2'
    else:
            lib_dir = 'lib/linux/arm/neon'
    ext_args = dict(        
        include_dirs=['include'],
        libraries = [lib_name],
        library_dirs = [lib_dir],
        extra_link_args = ["-Wl,-rpath=$ORIGIN"],
        define_macros = [('VERSION_INFO', __version__)],
        language='c++',
        cxx_std=11,
    )
    
# windows
elif sys.platform == "win":
    lib_dir = 'lib/win/x64/avx2'
    ext_args = dict(
        include_dirs=['include'], 
        libraries=[lib_name],
        library_dirs = [lib_dir],
        extra_link_args = ["-Wl,-rpath=$ORIGIN"],
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
        dst = os.path.join(self.build_lib, "yudet")
        copylibs(lib_dir, dst)
        filelist = os.listdir(self.build_lib)
        for file in filelist:
            filePath = os.path.join(self.build_lib, file)
            if not os.path.isdir(filePath):
                copylibs(filePath, dst)
                # delete file for wheel package
                os.remove(filePath)

# class CustomBuildExtDev(build_ext):
#     def run(self):
#         build_ext.run(self)
#         dev_folder = os.path.join(os.path.dirname(__file__), 'barcodeQrSDK')
#         copylibs(lib_dir, dev_folder)
#         filelist = os.listdir(self.build_lib)
#         for file in filelist:
#             filePath = os.path.join(self.build_lib, file)
#             if not os.path.isdir(file):
#                 copylibs(filePath, dev_folder)

# class CustomInstall(install):
#     def run(self):
#         install.run(self)

setup(
    name="yudet",
    keywords = ["face detection"],
    version = "0.0.1",
    author="Wwupup",
    author_email="12032501@mail.sustech.edu.cn",
    url="https://github.com/Wwupup/libfacedetection.pypi",
    description="A face detection library based on libfacedetection",
    license="BSD",
    packages=["yudet"],
    package_dir={"yudet": "src/yudet"},
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: C++",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Classifier: Operating System :: Microsoft :: Windows",
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Intended Audience :: Developers",
    ],
    ext_modules=yudet_modules, 
    cmdclass={'build_ext': CustomBuildExt}
)
