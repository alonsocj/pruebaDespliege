
from django.contrib.auth.decorators import login_required
import json
#from django.contrib import messages

from .models import Departamento, Dosis, Registro, Persona, Municipio, TipoVacuna

from django.views.generic.base import TemplateView
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import PersonaForm, PersonaForm1, RegistroForm1, PersonaForm2, PersonaForm3, RegistroForm2,VacunaForm1,VacunaForm2,DosisForm1
from django.contrib import messages

# Create your views here.
def login(request):
    return render(request,'login.html')

def logout(request):
    return render(request,'login.html')

class HomePage(TemplateView):
    object_list = Municipio
    template_name = "inicio.html"

    def dosisMunicipio(self):
        data = []
        for i in range(1,Municipio.objects.all().count()+1):
            person = Persona.objects.filter(id_municipio=i)
            
            prim =0
            segund = 0
            
            for p in range(0, person.count()):
                prim += Registro.objects.filter(dui = person[p],numero_dosis =1).count()
                segund += Registro.objects.filter(dui = person[p],numero_dosis =2).count()

            diccionario = {
                'mun': str(Municipio.objects.filter(id_municipio = i)[0]),
                'primDosis':prim,
                'segDosis':segund
                        }
            tojson =  json.dumps(diccionario)
            strjson = json.loads(tojson)
            data.append(strjson)
        return data

    def total_dosis(self):
        return self.cont_primerDosis() + self.cont_segundaDosis()

    def cont_primerDosis(self):
        return Registro.objects.filter(numero_dosis = 1).count()

    def cont_segundaDosis(self):
        return Registro.objects.filter(numero_dosis = 2).count()

    def cont_Mujeres(self):
        try:
            person = Persona.objects.filter(sexo = 'F')
            tot =0
            for i in range(0,person.count()):
                tot += Registro.objects.filter(dui = person[i]).count()

            averange = (tot/Registro.objects.filter().count())*100
            return averange
        except :
            return 0
    
    def cont_Hombres(self):
        try:
            person = Persona.objects.filter(sexo = 'M')
            tot =0
            for i in range(0,person.count()):
                tot += Registro.objects.filter(dui = person[i]).count()

            averange = (tot/Registro.objects.filter().count())*100
            return averange
        except :
            return 0
    
    def graf_vacunados(self):
        data = []
        try:
            for dep in range(1, Departamento.objects.all().count()+1):
                count = 0
                # se seleccionan los municipios relacionados con el departamento y se almacenan en un array de objetos tipo municipio
                datos = Municipio.objects.filter(id_departamento=Departamento.objects.get(id_departamento=dep))

                for mun in range(0, datos.count()):
                    # se hace un filtro de personas por municipio que estan relacionadas con el departamento que se esta iterando
                    person = Persona.objects.filter(id_municipio=datos[mun])
                    for p in range(0, person.count()):
                        count += Registro.objects.filter(dui = person[p]).count()

                # se almacena en un array los valores por departamento
                data.append(count)
        except:
            pass
        return data
          
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Home'] = 'Home'
        context['graf_vacunados'] = self.graf_vacunados()
        context['contador_Mujeres'] = self.cont_Mujeres()
        context['contador_Hombres'] = self.cont_Hombres()
        context['primer_dosis'] = self.cont_primerDosis()
        context['segunda_dosis'] = self.cont_segundaDosis()
        context['total_dosis'] = self.total_dosis()
        context['municipio1'] = self.dosisMunicipio()
        return context
      
class RegistrarPersona(CreateView):
    model = Persona
    template_name = 'personas/ingresarPersona.html'
    form_class = PersonaForm
    success_url = reverse_lazy('ConsultarPersona')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departamentos'] = Departamento.objects.all()
        context['municipios'] = Municipio.objects.all()
        return context

    def post(self, request, *args, **kwargs):
            self.object = self.get_object
            form = self.form_class(request.POST)
            if form.is_valid():
                persona = form.save()
                return HttpResponseRedirect(self.success_url)
            else:
                messages.warning(request, 'Ya existe una persona registrada con este dui')
                return self.render_to_response(self.get_context_data(form=form)) 

class ModificarPersona(UpdateView):
    model = Persona
    template_name = 'personas/modificarPersona.html'
    form_class = PersonaForm1
    success_url = reverse_lazy('ConsultarPersona')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departamentos'] = Departamento.objects.all()
        context['municipios'] = Municipio.objects.all()
        return context

class EliminarPersona(DeleteView):
    model = Persona
    second_model = Registro
    template_name = 'personas/eliminarPersona.html'
    form_class = PersonaForm
    success_url = reverse_lazy('ConsultarPersona')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = kwargs['pk']
        persona = self.model.objects.get(dui=pk)
        try:
            persona = self.model.objects.get(dui=pk)
            registro = self.second_model.objects.filter(dui=pk)
            a=len(registro)
            if(a==1):
                registro.delete()
                persona.delete()
            else:
                for re in registro:
                    re.delete()
                persona.delete()
            return HttpResponseRedirect(self.success_url)
        except self.model.DoesNotExist:
            persona = self.model.objects.get(dui=pk)
            persona.delete()
            return HttpResponseRedirect(self.success_url)

class ConsultarPersona(ListView):
    model = Persona
    template_name = 'personas/consultarPersona.html'

# vista del formulario de dosis 
class AgregarRegistro(CreateView):
    model = Registro
    second_model = Persona
    third_model = Dosis
    template_name = 'registro/agregarRegistro1.html'
    form_class = RegistroForm1
    second_form_class = PersonaForm2
    success_url = reverse_lazy('ConsultarRegistro')

    def get_context_data(self, **kwargs):
        context = super(AgregarRegistro, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        persona = self.second_model.objects.get(dui=pk)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=persona)
        context['id'] = pk
        return context   

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = kwargs['pk']
        persona = self.second_model.objects.get(dui=pk)
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST, instance=persona)
        if form.is_valid() and form2.is_valid():
            registro = form.save(commit=False)
            registro.dui = form2.save()
            a = form.cleaned_data['numero_dosis']
            if a.numero_dosis==1:
                try:
                    registro3 = self.model.objects.get(dui=pk, numero_dosis=form.cleaned_data['numero_dosis'])
                    messages.success(request, 'Ya existe un registro creado con la dosis ingresada')
                    return redirect('AgregarRegistro',pk)
                except:
                    registro.save()    
                    return HttpResponseRedirect(self.success_url)
            else:
                try:
                    registro1 = self.model.objects.get(dui=pk, numero_dosis=1)
                    try:
                        registro2 = self.model.objects.get(dui=pk, numero_dosis=form.cleaned_data['numero_dosis'])
                        messages.warning(request, 'Ya existe un registro creado con la dosis ingresada')
                        return redirect('AgregarRegistro',pk)
                    except:
                        try:
                            dosis = form.cleaned_data['numero_dosis']
                            a = int(dosis.numero_dosis)-1
                            dosis2 = self.third_model.objects.get(numero_dosis=a)
                            registro4 = self.model.objects.get(dui=pk, numero_dosis=dosis2)
                            if registro.nombre_vacuna == registro4.nombre_vacuna:
                                if registro.fecha_vacunacion > registro4.fecha_vacunacion:
                                    registro.save()
                                    return HttpResponseRedirect(self.success_url)
                                else: 
                                    messages.warning(request, 'La fecha debe ser posterior a la fecha registrada en la dosis anterior. La fecha de la dosis anterior es : '+str(registro4.fecha_vacunacion)+".")
                                    return redirect('AgregarRegistro', pk)
                            else:
                                messages.warning(request, 'El tipo de vacuna ingresada no coincide con el registrado en la dosis anterior. La vacuna registrada en la dosis anterior es : '+str(registro4.nombre_vacuna)+".")
                                return redirect('AgregarRegistro', pk)
                        except:
                            messages.warning(request, 'No puede registrar esta dosis si aun no ha registrado la anterior')
                            return redirect('AgregarRegistro', pk)
                except:
                    messages.warning(request, 'No existe dosis 1 registrada con este dui, ingrese la dosi 1 antes por favor')
                    return redirect('AgregarRegistro',pk)
        else:
            return redirect('AgregarRegistro',pk)

class IngresarDui(CreateView):
    model = Persona
    form_class = PersonaForm3
    template_name = 'registro/ingresarDui.html'
    success_url = reverse_lazy('IngresarDui')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        try:
            persona = self.model.objects.get(dui=request.POST.get('dui'))
            form = self.form_class(request.POST, instance=persona)
            if form.is_valid():
                    a = form.cleaned_data['dui']
                    return redirect('AgregarRegistro', a)
            else:
                messages.warning(request, 'Datos ingresados incorrectos')
                return HttpResponseRedirect(self.success_url)
        except self.model.DoesNotExist:
            messages.warning(request, 'El dui ingresado no esta registrado')
            return HttpResponseRedirect(self.success_url)

class ConsultarRegistro(ListView):
    model = Registro
    template_name = 'registro/consultarRegistro.html'

class ModificarRegistro(UpdateView):
    model = Registro
    second_model = Dosis
    template_name = 'registro/modificarRegistro.html'
    form_class = RegistroForm2
    success_url = reverse_lazy('ConsultarRegistro')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_re = kwargs['pk']
        registro = self.model.objects.get(id_registro=id_re)
        form = self.form_class(request.POST, instance=registro)
        if form.is_valid():
            registros = self.model.objects.filter(dui=registro.dui.dui)
            if registro.numero_dosis.numero_dosis == 1:
                for re in registros:
                    re.nombre_vacuna = form.cleaned_data['nombre_vacuna']
                    re.save()
                form.save()
                return HttpResponseRedirect(self.success_url)
            else:
                dosis = form.cleaned_data['numero_dosis']
                a = int(dosis.numero_dosis)-1
                dosis2 = self.second_model.objects.get(numero_dosis=a)
                registro2 = self.model.objects.get(dui = form.cleaned_data['dui'], numero_dosis = dosis2)

                if form.cleaned_data['nombre_vacuna'] == registro2.nombre_vacuna:
                    if form.cleaned_data['fecha_vacunacion'] > registro2.fecha_vacunacion:
                        form.save()
                        return HttpResponseRedirect(self.success_url)
                    else: 
                        messages.warning(request, 'La fecha debe ser posterior a la fecha registrada en la dosis anterior. La fecha de la dosis anterior es : '+str(registro2.fecha_vacunacion)+".")
                        return redirect('ModificarRegistro', id_re)
                else:
                    messages.warning(request, 'El tipo de vacuna ingresada no coincide con el registrado en la dosis anterior. La vacuna registrada en la dosis anterior es : '+str(registro2.nombre_vacuna)+".")
                    return redirect('ModificarRegistro', id_re)
        else:
            return HttpResponseRedirect(self.success_url)
          
#CRUD DE VACUNA
class ConsultarVacuna(ListView):
    model=TipoVacuna
    template_name='vacunas/consultarVacuna.html'
   
class AgregarVacuna(CreateView):
    model=TipoVacuna
    form_class=VacunaForm1
    template_name='vacunas/ingresarVacuna.html'
    success_url=reverse_lazy('ConsultarVacuna')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            persona = form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            messages.success(request, 'La vacuna ingresada ya esta registrada')
            return self.render_to_response(self.get_context_data(form=form))

class ModificarVacuna(UpdateView):
    model=TipoVacuna
    form_class=VacunaForm2
    template_name='vacunas/modificarVacuna.html'
    success_url=reverse_lazy('ConsultarVacuna')

class EliminarVacuna(DeleteView):
    model=TipoVacuna
    second_model = Registro
    template_name='vacunas/eliminarVacuna.html'
    success_url=reverse_lazy('ConsultarVacuna')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = kwargs['pk']
        vacuna = self.model.objects.get(nombre_vacuna=pk)
        try:
            registro = self.second_model.objects.filter(nombre_vacuna = vacuna.nombre_vacuna)
            if registro: 
                messages.warning(request, 'No se puede eliminar esta vacuna, existen registros asociados a ella')
                return redirect('EliminarVacuna', pk)
            else:
                vacuna.delete()
                return HttpResponseRedirect(self.success_url)
        except self.second_model.DoesNotExist:
                vacuna.delete()
                return HttpResponseRedirect(self.success_url)

#DOSIS
class ConsultarDosis(ListView):
    model=Dosis
    template_name='dosis/consultarDosis.html'

class AgregarDosis(CreateView):
    model=Dosis
    form_class=DosisForm1
    template_name='dosis/agregarDosis.html'
    success_url=reverse_lazy('ConsultarDosis')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            persona = form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            messages.success(request, 'La dosis ingresada ya esta registrada')
            return self.render_to_response(self.get_context_data(form=form))

class EliminarDosis(DeleteView):
    model=Dosis
    second_model = Registro
    template_name='dosis/eliminarDosis.html'
    success_url=reverse_lazy('ConsultarDosis')


    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = kwargs['pk']
        dosis = self.model.objects.get(numero_dosis=pk)
        try:
            registro = self.second_model.objects.filter(numero_dosis = dosis.numero_dosis)
            if registro: 
                messages.warning(request, 'No se puede eliminar esta dosis, existen registros asociados a ella')
                return redirect('EliminarDosis', pk)
            else:
                dosis.delete()
                return HttpResponseRedirect(self.success_url)
        except self.second_model.DoesNotExist:
                dosis.delete()
                return HttpResponseRedirect(self.success_url)

class EliminarRegistro(DeleteView):
    model = Registro
    second_model = Dosis
    template_name = 'registro/eliminarRegistro.html'
    form_class = RegistroForm1
    success_url = reverse_lazy('ConsultarRegistro')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_re = kwargs['pk']
        registro = self.model.objects.get(id_registro=id_re)
        if(registro.numero_dosis.numero_dosis == 1):
            try:
                registro1 = self.model.objects.get(dui=registro.dui, numero_dosis=2)
                messages.warning(request, 'Para eliminar el registro debe eliminar antes los registros de las otras dosis posteriores')
                return redirect('EliminarRegistro', id_re)
            except self.model.DoesNotExist:
                registro.delete()
                return HttpResponseRedirect(self.success_url)
        else:
            try:
                a = int(registro.numero_dosis.numero_dosis) + 1
                dosis = self.second_model.objects.get(numero_dosis = a)
                registro2 = self.model.objects.get(dui=registro.dui, numero_dosis=dosis)
                if registro2:
                    messages.warning(request, 'Para eliminar el registro debe eliminar antes los registros de las otras dosis posteriores')
                    return redirect('EliminarRegistro', id_re)
                else:
                    registro.delete()
                    return HttpResponseRedirect(self.success_url)
            except:
                registro.delete()
                return HttpResponseRedirect(self.success_url)

