from django import forms
from django.forms import ValidationError
from django.forms import ModelForm

from .models import GeneralContact, InsuranceContact


class GeneralContactForm(ModelForm):
    rodo_consent = forms.BooleanField(required=False)

    class Meta:
        model = GeneralContact
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Imię'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nazwisko'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nr. tel'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Twoja wiadomość'}),
        }

    def __init__(self, *args, **kwargs):
        super(GeneralContactForm, self).__init__(*args, **kwargs)
        self.fields['email'].error_messages = {'invalid': 'Niepoprawny adres email'}
        self.fields['phone'].error_messages = {'invalid': 'Niepoprawny numer telefonu'}

    def clean_rodo_consent(self):
        consent_given = self.cleaned_data['rodo_consent']
        if not consent_given:
            raise ValidationError('Należy zapoznać się z informacją o RODO', code='invalid')
        return consent_given


class OCACForm(ModelForm):
    class Meta:
        model = InsuranceContact
        fields = [
            'car_brand',
            'car_model',
            'car_mileage',
            'car_discounts',
            'car_engine_type',
            'car_engine_size',
            'year',
            'first_name',
            'last_name',
            'email',

        ]
        widgets = {
            'car_brand': forms.TextInput(attrs={'class': 'form-control col-md-8'}),
            'car_model': forms.TextInput(attrs={'class': 'form-control col-md-8'}),
            'car_mileage': forms.TextInput(attrs={'class': 'form-control col-md-8'}),
            'car_discounts': forms.TextInput(attrs={'class': 'form-control col-md-8'}),
            'car_engine_type': forms.Select(attrs={'class': 'form-control col-md-8'}),
            'car_engine_size': forms.TextInput(attrs={'class': 'form-control col-md-8'}),
            'year': forms.TextInput(attrs={'class': 'form-control col-md-8'}),

            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Imię'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nazwisko'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

    def __init__(self, *args, **kwargs):
        super(OCACForm, self).__init__(*args, **kwargs)

        # set all fields ar reqired
        for key in self.fields:
            self.fields[key].required = True

        # set Polish labels
        self.fields['car_brand'].label = 'Marka'
        self.fields['car_model'].label = 'Model'
        self.fields['car_mileage'].label = 'Przebieg (km)'
        self.fields['car_discounts'].label = 'Posiadane zniżki (%)'
        self.fields['car_engine_type'].label = 'Rodzaj silnika'
        self.fields['car_engine_size'].label = 'Pojemnośc silnika (cm3)'
        self.fields['year'].label = 'Rok produkcji'
        self.fields['first_name'].label = 'Imię'
        self.fields['last_name'].label = 'Nazwisko'

        self.fields['email'].error_messages = {'invalid': 'Niepoprawny adres email'}
