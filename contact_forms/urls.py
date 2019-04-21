from django.urls import path

from . import views


app_name = 'contact_forms'

urlpatterns = [
    path('oc-ac/', views.OCACContactCreate.as_view(), name='oc_ac_create'),
]
