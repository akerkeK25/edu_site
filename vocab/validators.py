from __future__ import annotations
import csv
from io import TextIOBase

ALLOWED_HEADERS = ['term', 'translation', 'example', 'image_url', 'deck']

class CSVFormatError(ValueError):
    """Исключение для некорректного CSV."""

def validate_csv(file_obj: TextIOBase) -> list[dict[str, str]]:
    """Проверяет CSV и возвращает список словарей-строк.
    Требует заголовок и хотя бы один непустой term/translation.
    """
    try:
        file_obj.seek(0)
        reader = csv.DictReader((line.decode('utf-8') for line in file_obj))
        headers = reader.fieldnames or []
    except Exception as exc:  # pylint: disable=broad-except
        raise CSVFormatError('Не удалось прочитать CSV как UTF-8.') from exc

    if not headers:
        raise CSVFormatError('Отсутствует заголовок CSV.')

    for h in headers:
        if h not in ALLOWED_HEADERS:
            raise CSVFormatError(f'Неожиданный столбец: {h}')

    rows: list[dict[str, str]] = []
    for idx, row in enumerate(reader, start=2):
        term = (row.get('term') or '').strip()
        translation = (row.get('translation') or '').strip()
        if not term or not translation:
            raise CSVFormatError(f'Строка {idx}: term/translation пустые.')
        rows.append(row)

    if not rows:
        raise CSVFormatError('CSV не содержит данных.')
    return rows
