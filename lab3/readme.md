# ЛР3. Создание своего пакета. Публикация на pypi

Пакет был создан па основе ЛР2.

был создан `__init__.py` и `setup.py`

Для начала нужно установить зависимости:
```bash
pip install setuptools wheel twine
```
После чего выполнить команду для сборки:
```bash
python setup.py sdist bdist_wheel
```
В результате в директории появятся новые папки: build, dist и p5l3_weatherdata_package.egg-info.

После чего нужно зарегестрироваться на Test PyPI и получить API-key, без него загрузить пакет не выйдет.

Когда появится API-key, можно выполнить следующую команду:
```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/* -u __token__ -p <API-key>
```
В результате её выполнения пакет загрузится, и к нему можно будет получить доступ:
https://test.pypi.org/project/p5l3-weatherdata-package/1.0/