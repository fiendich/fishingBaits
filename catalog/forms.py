from django import forms
from .models import Brand


class BrandFilterForm(forms.Form):
    brand_choices = [('', 'Все')] + [(brand.id, brand.name) for brand in Brand.objects.all()]
    brand = forms.ChoiceField(choices=brand_choices, required=False, widget=forms.Select(attrs={'class': 'form-control'}))

