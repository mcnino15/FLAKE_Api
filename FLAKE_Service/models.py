from django.db import models
from django.contrib.auth.models import User


class instituciones(models.Model):
    idinstitucion=models.AutoField(primary_key=True)
    instnombre=models.CharField(max_length=100)
    direccion= models.CharField(max_length=100)
    barrio=models.CharField(max_length=30)

class persona(models.Model):
    numid=models.CharField (max_length=30, primary_key=True)
    primer_nombre=models.CharField(max_length=30)
    segundo_nombre=models.CharField(max_length=30)
    primer_apellido=models.CharField(max_length=30)
    segundo_apellido=models.CharField(max_length=30)
    genero=models.CharField(max_length=10)
    fecha_nacimiento=models.DateField()
    estrato=models.CharField(max_length=5)

class tutor(persona):
    idtutor=models.AutoField(primary_key=True)
    telefono=models.CharField(max_length=30)
    correo=models.EmailField(unique=True)
    direccion=models.CharField(max_length=90)
    persona=models.ForeignKey(persona, on_delete=models.CASCADE, related_name='tutor_persona')
    instituciones=models.ForeignKey(instituciones, on_delete=models.CASCADE)

class administrador(persona):
    idadministrador=models.AutoField(primary_key=True)
    correo=models.EmailField(unique=True)
    persona=models.ForeignKey(persona, on_delete=models.CASCADE, related_name='administrador_persona')

class aula(models.Model):
    idaula=models.AutoField(primary_key=True)
    grado=models.CharField(max_length=60)
    gradunum=models.FloatField()
    grupo=models.FloatField()
    
    JORNADA_CHOICES = [
        ('D', 'Día'),
        ('T', 'Tarde'),
        ('N', 'Noche'),
        ('U', 'Unica'),
        ('X', 'No definido'),
    ]
    jornada = models.CharField(
        max_length=1,
        choices=JORNADA_CHOICES,
        default='D',
    )
    institucion=models.ForeignKey(instituciones, on_delete=models.CASCADE)
    tutor=models.ForeignKey(tutor,  on_delete=models.SET_NULL, null=True)

class estudiante (persona):
    idestudiante=models.AutoField(primary_key=True)
    persona=models.ForeignKey(persona, on_delete=models.CASCADE, related_name='estudiante_persona')
    instituciones=models.ForeignKey(instituciones, on_delete=models.CASCADE)
    aula=models.ForeignKey(aula, on_delete=models.SET_NULL, null=True)


class notas(models.Model):
    idnota=models.AutoField(primary_key=True)
    calificacion=models.FloatField()
    tutor=models.ForeignKey(tutor, on_delete=models.SET_NULL, null=True)

class asistencia(models.Model):
    idasistencia=models.AutoField(primary_key=True)
    ESTADOS_ASISTENCIA = [
        ('X', 'No se tomó asistencia'),
        ('A', 'No fue'),
        ('P', 'Sí fue'),
    ]
    estado = models.CharField(
        max_length=10,
        choices=ESTADOS_ASISTENCIA,
        default='NO_TOMADA'
    )
    fechaclase = models.DateField()
    tutor=models.ForeignKey(tutor, on_delete=models.SET_NULL, null=True)
    estudiante=models.ForeignKey(estudiante, on_delete=models.SET_NULL, null=True)

class horario(models.Model):
    idhorario=models.AutoField(primary_key=True)
    hora=models.TimeField()
    diainicial=models.CharField(max_length=2)
    diafinal=models.CharField(max_length=20)
    aula=models.ForeignKey(aula, on_delete=models.CASCADE)

class year_electivo(models.Model):
    idyear=models.AutoField(primary_key=True)
    year=models.FloatField()
    fechainicio=models.DateField()
    fechafin=models.DateField()
    numsemana=models.FloatField()





