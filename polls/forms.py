from django import forms
from .models import words_to_be_searched_model
class word_to_be_searched_form(forms.ModelForm):
    class Meta:
        model=words_to_be_searched_model

        fields=('word',)