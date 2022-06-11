from django.shortcuts import render, redirect
from .forms import CsvModelForm
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Csv
from BackendApp.models import Persona, Registro, Municipio, TipoVacuna, Dosis
import csv
from django.contrib import messages


# from django.http import HttpResponse
# Create your views here.


class DatosPersona(TemplateView):
    form_class = CsvModelForm
    template_name = 'csvs/csv.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = CsvModelForm()
            obj = Csv.objects.get(activated=False)
            with open(obj.file_name.path, 'r') as f:
                per = 0
                regis = 0
                vacum = 0
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    dui = row[0]
                    municipio = row[1]
                    nombre = row[2]
                    apellido = row[3]
                    sexo = row[4]
                    edad = row[5]
                    vacuna = row[6]
                    dosis = row[7]
                    fecha = row[8]
                    try:
                        Persona.objects.create(
                            dui=dui,
                            id_municipio=Municipio.objects.get(
                                id_municipio=municipio),
                            nombre=nombre,
                            apellido=apellido,
                            sexo=sexo,
                            edad=int(edad)
                        )
                    except:
                        # print('La Persona con el dui: '+str(dui)+', ya existe en la tabla de Personas')
                        per += 1
                        ban = False
                    try:
                        Registro.objects.filter(dui=dui)[0]

                    except:
                        ban = True

                    if ban:
                        try:
                            Registro.objects.create(
                                dui=Persona.objects.get(dui=dui),
                                nombre_vacuna=TipoVacuna.objects.get(
                                    nombre_vacuna=vacuna),
                                numero_dosis=Dosis.objects.get(numero_dosis=dosis),
                                fecha_vacunacion=fecha
                            )
                        except :
                            vacum +=1
                    else:
                        if dui == str(Registro.objects.filter(dui=dui)[0] and dosis == 1):
                            messages.warning(request, 'La Persona con el dui: '+str(dui) +
                                             ', ya existe en la tabla de Registros\n')
                            regis +=1
                        else:
                            Registro.objects.create(
                                dui=Persona.objects.get(dui=dui),
                                nombre_vacuna=TipoVacuna.objects.get(
                                    nombre_vacuna=vacuna),
                                numero_dosis=Dosis.objects.get(
                                    numero_dosis=dosis),
                                fecha_vacunacion=fecha
                            )
            obj.activated = True
            obj.save()
            if per == 0 or regis ==0 and vacum ==0: 
                messages.success(request,'Datos ingresados con exito')
            elif vacum > 0 :
                messages.warning(request,"Es posible que no se encuentre en la base de datos la vacuna asignada en un registro")

            return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upload-view'] = self.get()
        return context
