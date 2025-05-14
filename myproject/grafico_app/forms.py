from django import forms

class VectorForm(forms.Form):
    x = forms.FloatField(label='Coordenada X')
    y = forms.FloatField(label='Coordenada Y')
    z = forms.FloatField(label='Coordenada Z')