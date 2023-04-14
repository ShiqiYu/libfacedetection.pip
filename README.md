```shell
python -m build
twine upload --repository testpypi dist/*.gz
pip install -i https://test.pypi.org/simple/ yudet==0.0.1
pip install ./dist/yudet-0.0.1.tar.gz
```

## cross build toolchains:
* x86_64-linux: \
https://toolchains.bootlin.com/downloads/releases/toolchains/x86-64/tarballs/x86-64--glibc--stable-2022.08-1.tar.bz2\
* aarch64: \
https://toolchains.bootlin.com/downloads/releases/toolchains/aarch64/tarballs/aarch64--glibc--stable-2022.08-1.tar.bz2\
* armv7-eabihf:\
https://toolchains.bootlin.com/downloads/releases/toolchains/armv7-eabihf/tarballs/armv7-eabihf--glibc--stable-2022.08-1.tar.bz2

