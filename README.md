```shell
python -m build
twine upload --repository testpypi dist/*.gz
pip install -i https://test.pypi.org/simple/ yudet==0.0.1
pip install ./dist/yudet-0.0.1.tar.gz
```
