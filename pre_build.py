import platform
import os
import argparse
import shutil
import subprocess
from glob import glob

'''
 TODO:
    1. Support linux with arm and aarch64
    2. Support mac
    3. Support windows

'''

parser = argparse.ArgumentParser()
parser.add_argument('--platform', type=str, default=None, help='win, mac, linux')
parser.add_argument('--arch', type=str, default=None, help='x64, arm, aarch64')
parser.add_argument('--instruction_set', type=str, default=None, help='avx512, avx2, neon, native')
parser.add_argument('--build_all', action='store_true', help='build all platform, arch, instruction_set')
parser.add_argument('--src', type=str, default='./libfacedetection', help='source dir')

project_dir = os.path.abspath(os.path.dirname(__file__))
def keep_dir_exist(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def get_platform():
    if platform.system() == 'Windows':
        return 'win'
    elif platform.system() == 'Darwin':
        return 'mac'
    elif platform.system() == 'Linux':
        return 'linux'
    else:
        return 'unknown'

def get_arch():
    if platform.machine() == 'AMD64' or platform.machine() == 'x86_64':
        return 'x64'
    elif platform.machine() == 'aarch64':
        return 'aarch64'
    else:
        return 'arm'

def get_instruction_set():
    if platform.machine() == 'AMD64' or platform.machine() == 'x86_64':
        return 'avx2'
    else:
        return 'neon'

def check_env():
    print("""python version: %s
python branch: %s
python build version: %s
python compiler version: %s
python implementation: %s
""" % (
platform.python_version(),
platform.python_branch(),
platform.python_build(),
platform.python_compiler(),
platform.python_implementation(),
))

print("""os: %s
os kernel version: %s
os release version: %s
os platform: %s
mac version: %s
uname: %s
architecture: %s
machine: %s
""" % (
platform.system(),
platform.version(),
platform.release(),
platform.platform(),
platform.mac_ver(),
platform.uname(),
platform.architecture(),
platform.machine(),
))

def cross_build(plat, arch, instruction_set):

    if plat == 'linux' and arch == 'x64':
        toolchain_file = os.path.abspath('./toolchains/x86-64--glibc--stable-2022.08-1/x86_64-linux.toolchain.cmake')
    elif plat == 'linux' and arch == 'aarch64':
        toolchain_file = os.path.abspath('./toolchains/aarch64--glibc--stable-2022.08-1/aarch64-linux.toolchain.cmake')
    elif plat == 'linux' and arch == 'arm':
        toolchain_file = os.path.abspath('./toolchains/armv7-eabihf--glibc--stable-2022.08-1/armv7-eabihf-linux.toolchain.cmake')
    elif plat == 'win' and arch == 'x64':
        toolchain_file = os.path.abspath('./toolchains/x86-64--msvc--latest/x86-64-windows.toolchain.cmake')
    else:
        raise Exception('Not support plat: {}, arch: {}'.format(plat, arch))
    
    library_dir = os.path.abspath('lib/{}/{}/{}'.format(plat, arch, instruction_set))
    include_dir = os.path.abspath('include')

    cmake_args = [
        '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={}'.format(library_dir),
        '-DCMAKE_BUILD_TYPE=Release',
        '-DBUILD_SHARED_LIBS=ON',
        '-DDEMO=OFF',
        '-DCMAKE_TOOLCHAIN_FILE={}'.format(toolchain_file)
    ]
    
    if instruction_set == 'avx512':
        cmake_args.append('-DENABLE_AVX512=ON')
        cmake_args.append('-DENABLE_AVX2=OFF')
        cmake_args.append('-DENABLE_NEON=OFF')
    elif instruction_set == 'avx2':
        cmake_args.append('-DENABLE_AVX512=OFF')
        cmake_args.append('-DENABLE_AVX2=ON')
        cmake_args.append('-DENABLE_NEON=OFF')
    elif instruction_set == 'neon':
        cmake_args.append('-DENABLE_AVX512=OFF')
        cmake_args.append('-DENABLE_AVX2=OFF')
        cmake_args.append('-DENABLE_NEON=ON')
    elif instruction_set == 'native':
        cmake_args.append('-DENABLE_AVX512=OFF')
        cmake_args.append('-DENABLE_AVX2=OFF')
        cmake_args.append('-DENABLE_NEON=OFF')
    else:
        raise Exception('Not support instruction_set: {}'.format(instruction_set))
    
    keep_dir_exist(library_dir)
    keep_dir_exist(include_dir)
    build_dir = os.path.abspath('build')
    keep_dir_exist(build_dir)
    src_dir = os.path.abspath(args.src)
    try:
        subprocess.check_call(['cmake', '-S', src_dir] + cmake_args, cwd=build_dir)
        subprocess.check_call(['cmake', '--build', build_dir, '--config', 'Release'], cwd=project_dir)
    except subprocess.CalledProcessError as e:
        print(e)
        raise Exception('Build failed')
    
    export_header_file = glob(os.path.join(build_dir, '*.h'))[0]
    header_file = glob(os.path.join(src_dir, 'src', '*.h'))[0]
    shutil.copy2(export_header_file, os.path.join(include_dir, os.path.basename(export_header_file)))
    shutil.copy2(header_file, os.path.join(include_dir, os.path.basename(header_file)))
    shutil.rmtree(build_dir)


if __name__ == "__main__":
    args = parser.parse_args()
    check_env()
    if args.build_all:
        build_target = [
            ('linux', 'x64', 'avx2'),
            ('linux', 'x64', 'avx512'),
            ('linux', 'x64', 'native'),
            ('linux', 'arm', 'neon'),
            ('win', 'x64', 'avx2'),
            ('win', 'x64', 'avx512'),
            ('win', 'x64', 'native'),
        ]
    elif args.platform is not None and args.arch is not None and args.instruction_set is not None:
        build_target = [(args.platform, args.arch, args.instruction_set)]
    elif args.platform is None and args.arch is None and args.instruction_set is None:
        build_target = [(get_platform(), get_arch(), get_instruction_set())]
    else:
        raise Exception('Please specify platform, arch, instruction_set or use --build_all or leave all args empty.')
    
    print('local platform: {}'.format(get_platform()))
    print('local arch: {}'.format(get_arch()))
    print('local instruction_set: {}'.format(get_instruction_set()))

    for plat, arch, instruction_set in build_target:
        print('\nbuild for plat: {}, arch: {}, instruction_set: {}'.format(plat, arch, instruction_set))
        try:
            cross_build(plat, arch, instruction_set)
        except Exception as e:
            print(e)




    