```shell
pip install cibuildwheel
cibuildwheel --platform linux

twine upload --repository testpypi dist/*.gz
pip install -i https://test.pypi.org/simple/ yuface==0.0.1
```