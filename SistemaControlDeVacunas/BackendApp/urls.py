from os import name
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from Import_Csv import urls
from .views import  AgregarVacuna ,ConsultarVacuna,ModificarVacuna,EliminarVacuna,ConsultarDosis,AgregarDosis,EliminarDosis
from .views import HomePage, RegistrarPersona, ConsultarPersona, ModificarPersona, EliminarPersona
from.views import AgregarRegistro, IngresarDui, ConsultarRegistro, ModificarRegistro, EliminarRegistro


urlpatterns = [
#Persona
    path('', HomePage.as_view(), name = 'Home'),
    path('registrarpersona/', login_required(RegistrarPersona.as_view()), name = 'RegistrarPersona'),
    path('consultarpersona/', login_required(ConsultarPersona.as_view()), name = 'ConsultarPersona'),
    path('modificarpersona/<str:pk>/', login_required(ModificarPersona.as_view()), name = 'ModificarPersona'),
    path('eliminarpersona/<str:pk>/', login_required(EliminarPersona.as_view()), name = 'EliminarPersona'),

#Vacuna
    path('agregarVacuna/', login_required(AgregarVacuna.as_view()), name = 'AgregarVacuna'),
    path('consultarVacuna/', login_required(ConsultarVacuna.as_view()), name = 'ConsultarVacuna'),
    path('modificarVacuna/<str:pk>/', login_required(ModificarVacuna.as_view()), name = 'ModificarVacuna'),
    path('eliminarVacuna/<str:pk>/', login_required(EliminarVacuna.as_view()), name = 'EliminarVacuna'),


#Dosis
    path('consultardosis/', login_required(ConsultarDosis.as_view()), name = 'ConsultarDosis'),
    path('agregardosis/', login_required(AgregarDosis.as_view()), name = 'AgregarDosis'),
    path('eliminardosis/<int:pk>/', login_required(EliminarDosis.as_view()), name = 'EliminarDosis'),

#Registro
    path('ingresardui/', login_required(IngresarDui.as_view()), name = 'IngresarDui'),
    path('agregarregistro/<str:pk>/',login_required(AgregarRegistro.as_view()), name = 'AgregarRegistro'),
    path('consultarregistro/', login_required(ConsultarRegistro.as_view()), name = 'ConsultarRegistro'),
    path('modificarregistro/<str:pk>/', login_required(ModificarRegistro.as_view()), name = 'ModificarRegistro'),
    path('eliminarregistro/<str:pk>/', login_required(EliminarRegistro.as_view()), name = 'EliminarRegistro'),
]
