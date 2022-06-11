from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import DatosPersona

from BackendApp.views import HomePage

app_name = 'csvs'

urlpatterns=[
    path('', HomePage.as_view(), name='Home'),
    path('csv/',login_required(DatosPersona.as_view()), name='upload-view'),

]