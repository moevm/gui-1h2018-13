# gui-1h2018-13
## Мессенджер для ВКонтакте.
Данная программа требует Python 3.5.
Данная верия Python является предустановленной на Ubuntu 16.04+, nакже она использует 2 зависимости: **vk**, **PyQt5**.
* Скачать Python можно [здесь](https://www.python.org/).
### Запуск Linux (Debian-based).
* Требуется установить инструмент *pip*:
``` 
sudo apt install python3-pip
```
* Скачаем специализированный пакет: 
```
sudo pip3 install virtualenv
```
* В корне проекта требуется ввести 
```
virtualenv venv
```
* Появится папка *venv*, которая содержит в себе интерпретатор Python.
* Выполнить команду:
```
source ./venv/bin/activate
```
* Загрузить зависимости:
```
pip install vk, PyQt5
```
* Запустить программу:
```
python main.py
```
### Запуск Windows.

* Скачать Python 3.5+ [тык](https://www.python.org/).
* Скачаем специализированный пакет: 
```
pip install virtualenv
```
* В корне проекта требуется ввести:
```
virtualenv venv
```
* Появится папка *venv*, которая содержит в себе интерпретатор Python.
* Выполнить команду:
```
./venv/Scripts/activate
```
* Загрузить зависимости:
```
pip install vk, PyQt5
```
* Запустить программу:
```
python main.py
```
