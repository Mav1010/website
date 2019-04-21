from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='homepage'),
    path('ajax_send_contact_form', views.ajax_send_contact_form, name='ajax_send_contact_form'),
    path('contact/', include('contact_forms.urls')),
]
