# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Departamento(models.Model):
    id_departamento = models.IntegerField(primary_key=True)
    nombre_departamento = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'departamento'

    def __str__(self) :
        return self.nombre_departamento


class Dosis(models.Model):
    numero_dosis = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'dosis'
    
    def __str__(self) :
        return '{}'.format(self.numero_dosis)


class Municipio(models.Model):
    id_municipio = models.IntegerField(primary_key=True)
    id_departamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='id_departamento', blank=True, null=True)
    nombre_municipio = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'municipio'

    def __str__(self) :
        return self.nombre_municipio


class Persona(models.Model):
    dui = models.CharField(primary_key=True, max_length=10)
    id_municipio = models.ForeignKey(Municipio, models.DO_NOTHING, db_column='id_municipio', blank=True, null=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    sexo = models.CharField(max_length=1)
    edad = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'persona'

    def __str__(self):
        return '{}'.format(self.dui)


class Registro(models.Model):
    id_registro = models.AutoField(primary_key=True)
    dui = models.ForeignKey(Persona, models.DO_NOTHING, db_column='dui', blank=True, null=True)
    nombre_vacuna = models.ForeignKey('TipoVacuna', models.DO_NOTHING, db_column='nombre_vacuna', blank=True, null=True)
    numero_dosis = models.ForeignKey(Dosis, models.DO_NOTHING, db_column='numero_dosis', blank=True, null=True)
    fecha_vacunacion = models.DateField()

    class Meta:
        managed = False
        db_table = 'registro'
        
    def __str__(self):
        return '{}'.format(self.dui)


class TipoVacuna(models.Model):
    nombre_vacuna = models.CharField(primary_key=True, max_length=50)
    fabricante = models.CharField(max_length=50)
    pais_fabricacion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tipo_vacuna'

    def __str__(self) :
        return self.nombre_vacuna

