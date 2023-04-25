#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.build_ext import build_ext
from setuptools.command.install import install
from pybind11.setup_helpers import Pybind11Extension

from glob import glob
import subprocess
import os
import platform
import sys
import shutil

__version__ = "0.0.1"

root_dir = os.path.dirname(os.path.abspath(__file__))

cmake_args = [
    '-DCMAKE_BUILD_TYPE=Release',
    '-DBUILD_SHARED_LIBS=ON',
    '-DDEMO=OFF',
]

# linux
if sys.platform == "linux" or sys.platform == "linux2":
    if platform.uname()[4] == 'AMD64' or platform.uname()[4] == 'x86_64' or platform.uname()[4] == 'aarch64':
        cmake_args.append('-DENABLE_AVX2=ON')
        cmake_args.append('-DENABLE_AVX512=OFF')
        cmake_args.append('-DENABLE_NEON=OFF')
    else:
        cmake_args.append('-DENABLE_AVX2=OFF')
        cmake_args.append('-DENABLE_AVX512=OFF')
        cmake_args.append('-DENABLE_NEON=ON')
    ext_args = dict(        
        extra_link_args = ["-Wl,-rpath=$ORIGIN"],
        define_macros = [('VERSION_INFO', __version__)],
        language='c++',
        cxx_std=11,
    )
    
# windows
elif sys.platform == "win":
    cmake_args.append('-DENABLE_AVX2=ON')
    cmake_args.append('-DENABLE_AVX512=OFF')
    cmake_args.append('-DENABLE_NEON=OFF')
    ext_args = dict(
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

def build_submodule(ext:build_ext):
    src_dir = os.path.join(root_dir, 'libfacedetection')
    build_dir_submodule = os.path.join(os.path.abspath(ext.build_temp), 'libfacedetection')
    if not os.path.exists(build_dir_submodule):
        os.makedirs(build_dir_submodule)

    include_dir = os.path.join(build_dir_submodule, 'include')
    lib_dir = os.path.join(build_dir_submodule, 'lib')

    cmake_args.append('-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + lib_dir)
    subprocess.check_call(['cmake', '-S', src_dir] + cmake_args, cwd=build_dir_submodule)
    subprocess.check_call(['cmake', '--build', build_dir_submodule, '--config', 'Release'], cwd=build_dir_submodule)

    # copy header file
    if not os.path.exists(include_dir):
        os.makedirs(include_dir)
    export_header_file = glob(os.path.join(build_dir_submodule, '*.h'))[0]
    header_file = glob(os.path.join(src_dir, 'src', '*.h'))[0]
    shutil.copy2(export_header_file, os.path.join(include_dir, os.path.basename(export_header_file)))
    shutil.copy2(header_file, os.path.join(include_dir, os.path.basename(header_file)))

    ext.include_dirs.append(include_dir)
    ext.library_dirs.append(lib_dir)
    ext.libraries.append('facedetection')

class CustomBuildExt(build_ext):
    def run(self):
        build_submodule(self)
        build_ext.run(self)

        dst = os.path.join(self.build_lib, "yudet")

        # copy dynamic libs
        copylibs(self.library_dirs[0], dst)

        # move generated extension libs
        filelist = os.listdir(self.build_lib)
        for file in filelist:
            filePath = os.path.join(self.build_lib, file)
            if not os.path.isdir(filePath):
                copylibs(filePath, dst)
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
    license="./LISENCE",
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
