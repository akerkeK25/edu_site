from __future__ import annotations
from django import forms
from .models import Card, Deck
from .validators import validate_csv, CSVFormatError

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['deck', 'term', 'translation', 'example', 'image_url']

    def clean_term(self):
        term = self.cleaned_data['term'].strip()
        if len(term) < 2:
            raise forms.ValidationError('Слово слишком короткое.')
        return term

    def clean_translation(self):
        translation = self.cleaned_data['translation'].strip()
        if len(translation) < 2:
            raise forms.ValidationError('Перевод слишком короткий.')
        return translation

class CSVUploadForm(forms.Form):
    file = forms.FileField(label='CSV файл')

    def clean_file(self):
        file_ = self.cleaned_data['file']
        try:
            rows = validate_csv(file_)
        except CSVFormatError as exc:
            raise forms.ValidationError(str(exc)) from exc
        self.cleaned_data['rows'] = rows
        return file_

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if len(name) < 2:
            raise forms.ValidationError('Название слишком короткое.')
        return name
