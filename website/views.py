from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt

from contact_forms.forms import GeneralContactForm
from contact_forms.models import GeneralContact
from contact_forms.utils import send_email_sendgrid


def home_page(request):

    map_key = settings.MAP_KEY
    form = GeneralContactForm()

    context = {
        'map_key': map_key,
        'form': form
    }
    return render(request, 'index.html', context)


@csrf_exempt
def ajax_send_contact_form(request):
    if request.is_ajax():
        form = GeneralContactForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            data['general'] = True
            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']
            phone = data['phone']
            message = data['message']

            # create instance of GeneralContact
            try:
                GeneralContact.objects.create(first_name=first_name,
                                              last_name=last_name,
                                              email=email,
                                              phone=phone,
                                              message=message)
            except Exception as error:
                send_email_sendgrid('error@website.pl', settings.ADMIN_RECIPIENT_EMAIL, 'Error in General Form',
                                    'text/html', '{}: {}'.format(error, type(error)))

            # send email with notification:
            subject = 'Formularz kontaktowy od: {} {}'.format(first_name, last_name)
            context = {
                'data': data
            }
            message_body = get_template('contact_forms/email_template.html').render(context)
            send_email_sendgrid(email, settings.AGENT_RECIPIENT_EMAIL, subject,
                                'text/html', message_body)
            return JsonResponse({'success': True})

        else:
            return JsonResponse({'error': form.errors})

    else:
        return HttpResponse('request is not ajax')

