from __future__ import annotations
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .validators import validate_csv, CSVFormatError

class CSVValidateTests(TestCase):
    def test_ok(self):
        content = (
            'term,translation,example\n'
            'cat,кошка,The cat sleeps.\n'
        ).encode('utf-8')
        rows = validate_csv(SimpleUploadedFile('t.csv', content))
        self.assertEqual(len(rows), 1)

    def test_bad_columns(self):
        content = 'foo,bar\n1,2\n'.encode('utf-8')
        with self.assertRaises(CSVFormatError):
            validate_csv(SimpleUploadedFile('t.csv', content))
