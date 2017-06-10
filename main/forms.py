from django import forms

class WordsForm(forms.Form):
    first_word = forms.CharField(label='Начальное понятие', max_length=100)
    last_word = forms.CharField(label='Дополнительное понятие', max_length=100)
    max_level = forms.IntegerField(label='Максимальный уровень', initial=3)
    coefficient = forms.FloatField(label='Коэффициент принадлежности', initial=0.6)
    file = forms.FileField(label='Файл онтологии')
