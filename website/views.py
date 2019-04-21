from django.conf import settings
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage

from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from contact_forms.forms import GeneralContactForm
from contact_forms.models import GeneralContact


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
                send_mail('Error in General Form', '{}: {}'.format(error, type(error)), settings.ADMIN_RECIPIENT_EMAIL,
                          [settings.ADMIN_RECIPIENT_EMAIL])

            # send email with notification:
            subject = 'Formularz kontaktowy od: {} {}'.format(first_name, last_name)
            context = {
                'data': data
            }
            message_body = render_to_string('contact_forms/email_template.html', context=context)

            mail = EmailMessage(
                subject,
                message_body,
                settings.ADMIN_RECIPIENT_EMAIL,
                [settings.AGENT_RECIPIENT_EMAIL],
                [settings.ADMIN_RECIPIENT_EMAIL]
            )
            mail.send()

            return JsonResponse({'success': True})

        else:
            return JsonResponse({'error': form.errors})

    else:
        return HttpResponse('request is not ajax')

