from django.db import models

from . import choices as choices_forms
from core.models import BaseContactMessage


class GeneralContact(BaseContactMessage):
    message = models.CharField(max_length=3000)

    def __str__(self):
        return('Kontakt {} {} ({})'.format(self.first_name, self.last_name, self.date_created.date()))


class InsuranceContact(BaseContactMessage):
    type = models.IntegerField(choices=choices_forms.INSURANCE_TYPE)

    # OC/AC
    car_brand = models.CharField(max_length=50, blank=True, null=True)
    car_model = models.CharField(max_length=50, blank=True, null=True)
    car_mileage = models.CharField(max_length=30, blank=True, null=True)
    car_discounts = models.CharField(max_length=50, blank=True, null=True)
    car_engine_type = models.IntegerField(choices=choices_forms.ENGINE_TYPE, blank=True, null=True)
    car_engine_size = models.CharField(max_length=50, blank=True, null=True)

    # Dom/Mieszkanie
    house_size = models.CharField(max_length=50, blank=True, null=True)
    house_worth = models.CharField(max_length=50, blank=True, null=True)

    # NNW/Na Życie
    age = models.IntegerField(blank=True, null=True)
    profession = models.CharField(max_length=150, blank=True, null=True)

    # General
    year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return('Kontakt {} {} ({})'.format(self.type, self.last_name, self.date_created.date()))