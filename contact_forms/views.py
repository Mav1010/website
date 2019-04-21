from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage

from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.generic import FormView

from . import choices as choices_forms
from .forms import OCACForm
from .models import InsuranceContact


class OCACContactCreate(FormView):
    template_name = 'contact_forms/base_form.html'
    form_class = OCACForm

    def form_valid(self, form):
        data = form.cleaned_data
        data['type'] = 'OC/AC'
        type = data['type']
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        car_brand = data['car_brand']
        car_model = data['car_model']
        car_mileage = data['car_mileage']
        car_discounts = data['car_discounts']
        car_engine_type = data['car_engine_type']
        car_engine_size = data['car_engine_size']
        year = data['year']

        # create instance of GeneralContact
        try:
            InsuranceContact.objects.create(type=choices_forms.OC_AC,
                                            first_name=first_name,
                                            last_name=last_name,
                                            email=email,
                                            car_brand=car_brand,
                                            car_model=car_model,
                                            car_mileage=car_mileage,
                                            car_discounts=car_discounts,
                                            car_engine_type=car_engine_type,
                                            car_engine_size=car_engine_size,
                                            year=year,
                                            )
        except Exception as error:
            send_mail('Błąd w formularzu OC/AC', '{}: {}'.format(error, type(error)), settings.ADMIN_RECIPIENT_EMAIL, [settings.AGENT_RECIPIENT_EMAIL])

        # send email with notification:
        subject = 'Formularz OC/AC od: {} {}'.format(first_name, last_name)
        context = {
            'data': data,
        }
        message = render_to_string('contact_forms/email_template.html', context=data)
        mail = EmailMessage(
            subject,
            message,
            settings.ADMIN_RECIPIENT_EMAIL,
            [settings.AGENT_RECIPIENT_EMAIL],
            [settings.ADMIN_RECIPIENT_EMAIL]
        )
        mail.send()

        messages.success(self.request, 'Dziękujemy za przesłanie formularza. Skontaktujemy się z Tobą wkrótce.')
        return redirect('contact_forms:oc_ac_create')

    def form_invalid(self, form):
        return super(OCACContactCreate, self).form_invalid(form)

