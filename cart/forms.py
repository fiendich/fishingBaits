from django import forms


class OrderForm(forms.Form):
    full_name = forms.CharField(label='ФИО')
    phone_number = forms.CharField(label='Номер телефона')
    email = forms.EmailField(label='Email', required=False)
    address = forms.CharField(label='Адрес', widget=forms.Textarea)
