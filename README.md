# Портал для абитуриентов 
В текущий момент не существует удобного сайта, способного предоставлять информацию для абитуриентов в удобном виде.  
**Идея** - создать портал, автоматически агрегирующий различную информацию из множества источников о специальностях, ВУЗах, направлениях, и предоставляющий эту информацию для абитуриентов.

## Contributors
[toert](https://github.com/toert) - Django, JavaScript  
[PoFF](https://github.com/poffk) - Data Mining, Django  
[FnrYoto](https://github.com/Ilya-Gr) - Design, HTML&CSS, JavaScript 

## Планируемый функционал
* Калькулятор баллов ЕГЭ и получение списка направлений/ВУЗов, на которые абитуриент способен поступить
* Перевод первичных баллов в тестовые(по 100-балльной шкале)
* Сравнение различных специальностей в разных ВУЗах
* Сравнение различных специальностей в общем

## Основная информация
### Список ВУЗов
С [postyplenie](http://postyplenie.ru):
* Название вуза

С [graduate](http://vo.graduate.edu.ru):
* Доля трудоустройства выпускников
* Средняя З/П выпускников (за год после выпуска)
* Средний возраст выпускников

Заполняем вручную:
* Начиличие военной кафедры
* Наличие общежития

### Список специальностей
**Информация о специальность в общем:**
* Код специальности

С [Яндекс Работы](https://rabota.yandex.ru/):
* З/П

С [moeobrazovanie](https://moeobrazovanie.ru/)(?):
* Рейтинг специальности
* Вступительные экзамены
* Будущие профессии
* Основные учебные предметы

**Информация о специальности в каждом вузе:**
* Название вуза

С [postyplenie](http://postyplenie.ru):
* Количество мест
* Количество человек на место
* Факультет
* Минимальный проходной балл 1ой волны
* Наличие/отсутствие и минимальный проходной балл 2ой волны

С [graduate](http://vo.graduate.edu.ru):
* З/П
* Доля трудоустройства
* Средний возраст выпускников

Заполняем вручную:
* (?) Станция метро, на которой проходит обучение

## Features
### Перевод баллов 
### Сравнение ВУЗов
### Сравнение специальностей 

# Getting started

Добавьте в ваше окружение среды переменную `DJANGO_SETTINGS_MODULE` равную `config.settings.local`. [Как это сделать в Windows?](http://ru.stackoverflow.com/questions/153628/%D0%9A%D0%B0%D0%BA-%D0%B4%D0%BE%D0%B1%D0%B0%D0%B2%D0%B8%D1%82%D1%8C-%D0%B2-%D0%BF%D0%B5%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D1%83%D1%8E-%D0%BE%D0%BA%D1%80%D1%83%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F-path-%D0%BF%D1%83%D1%82%D1%8C) [Unix?](http://ru.stackoverflow.com/questions/228/%D0%9A%D0%B0%D0%BA-%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%B8%D1%82%D1%8C-%D0%BF%D0%B5%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D1%83%D1%8E-%D0%BE%D0%BA%D1%80%D1%83%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B2-linux-unix).  
Создаем БД, вводя данные строки в консоль psql:
```
CREATE DATABASE ege_db;
CREATE USER admin WITH PASSWORD 'admin1703’;
GRANT ALL PRIVILEGES ON DATABASE ege_db TO admin;
```
Затем вводите команды в командную строку:

```sh
git clone https://github.com/toert/ege-portal.git
python3 -m venv venv
# Windows:
venv\Scripts\activate
# Unix:
source venv/bin/activate

cd ege-portal
pip3 install -r requirements.txt
python3 manage.py migrate
```
