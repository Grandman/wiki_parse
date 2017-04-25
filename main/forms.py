from django import forms

class WordsForm(forms.Form):
    first_word = forms.CharField(label='First word', max_length=100)
    last_word = forms.CharField(label='Last word', max_length=100)
    file = forms.FileField()
