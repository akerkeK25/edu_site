# Edu Site — Django Flashcards & Quiz (Учебный проект)

Веб‑сервис на Django для изучения английских слов: создание своих колод, загрузка CSV с карточками (Anki‑подобно), тренировка с автоматической проверкой ответа и статистикой.

## Запуск
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Откройте http://127.0.0.1:8000

## CSV формат
Файл **UTF‑8** с заголовком:
```
term,translation,example,image_url,deck
```
Столбцы `example`, `image_url` — опциональные; `deck` — имя колоды.
