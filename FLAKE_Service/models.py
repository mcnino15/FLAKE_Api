from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Instituciones(models.Model):
    idinstitucion=models.AutoField(primary_key=True)
    instnombre=models.CharField(max_length=100)
    direccion= models.CharField(max_length=100)
    barrio=models.CharField(max_length=30)

class PersonaManager(BaseUserManager):
    def create_user(self, cedula, password=None, **extra_fields):
        if not cedula:
            raise ValueError('The Cedula field must be set')
        user = self.model(cedula=cedula, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cedula, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(cedula, password, **extra_fields)

class Persona(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    cedula = models.CharField(max_length=30, unique=True)
    primer_nombre = models.CharField(max_length=30)
    segundo_nombre = models.CharField(max_length=30, blank=True, null=True)
    primer_apellido = models.CharField(max_length=30)
    segundo_apellido = models.CharField(max_length=30, blank=True, null=True)
    genero = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])
    fecha_nacimiento = models.DateField()
    estrato = models.CharField(max_length=5)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

  
    groups = models.ManyToManyField(    
        'auth.Group',
        related_name='persona_set',
        blank=True,
        help_text='Los grupos a los que pertenece este usuario.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='persona_permissions_set',
        blank=True,
        help_text='Permisos específicos para este usuario.'
    )

    objects = PersonaManager()

    USERNAME_FIELD = 'cedula'
    REQUIRED_FIELDS = ['primer_nombre', 'primer_apellido']

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido} ({self.numid})"

class Aula(models.Model):
    idaula=models.AutoField(primary_key=True)
    grado=models.CharField(max_length=60)
    gradunum=models.FloatField()
    grupo=models.FloatField()
    
    JORNADA_CHOICES = [
        ('D', 'Día'),
        ('T', 'Tarde'),
        ('U', 'Unica'),
        ('X', 'No definido'),
    ]
    jornada = models.CharField(
        max_length=1,
        choices=JORNADA_CHOICES,
        default='D',
    )
    institucion=models.ForeignKey(Instituciones, on_delete=models.CASCADE)
    
       
class Tutor(models.Model):
    idtutor = models.AutoField(primary_key=True)
    telefono = models.CharField(max_length=30)
    correo = models.EmailField(unique=True)
    direccion = models.CharField(max_length=90)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name='tutor_profile')
    instituciones = models.ForeignKey(Instituciones, on_delete=models.SET_NULL, null=True, blank=True)
    aula = models.ForeignKey(Aula, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Tutor: {self.persona.primer_nombre} {self.persona.primer_apellido}"

class Administrador(models.Model):
    idadministrador = models.AutoField(primary_key=True)
    correo = models.EmailField(unique=True)
    
    # Relación uno a uno con Persona
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name='admin_profile')

    def __str__(self):
        return f"Administrador: {self.persona.primer_nombre} {self.persona.primer_apellido}"




class Estudiante(models.Model):
    idestudiante = models.AutoField(primary_key=True)
    instituciones = models.ForeignKey(Instituciones, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.SET_NULL, null=True, blank=True)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name='estudiante_profile')

    def __str__(self):
        return f"Estudiante: {self.persona.primer_nombre} {self.persona.primer_apellido}"


class Notas(models.Model):
    idnota = models.AutoField(primary_key=True)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='notas')
    bloque1 = models.FloatField(null=True, blank=True)
    bloque2 = models.FloatField(null=True, blank=True)
    bloque3 = models.FloatField(null=True, blank=True)
    bloque4 = models.FloatField(null=True, blank=True)
    aula = models.ForeignKey(Aula, on_delete=models.SET_NULL, null=True, blank=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.SET_NULL, null=True)
    calificacion_final = models.FloatField(null=True, blank=True)  # Calificación final

    def calcular_calificacion_final(self):
        # Verifica que todos los bloques tengan calificación
        if all([self.bloque1 is not None, self.bloque2 is not None, self.bloque3 is not None, self.bloque4 is not None]):
            if self.bloque1 == 0 and self.bloque2 == 0 and self.bloque3 == 0 and self.bloque4 == 0:
                self.calificacion_final = 0
            else:
            # Ponderación de cada bloque (25% por bloque)
                self.calificacion_final = (self.bloque1 + self.bloque2 + self.bloque3 + self.bloque4) / 4
            self.save()
        else:
            # Si no están todas las notas, no se puede calcular la calificación final
            self.calificacion_final = None
            self.save()

    def __str__(self):
        return f"Notas de {self.estudiante.persona.primer_nombre} {self.estudiante.persona.primer_apellido}"

class asistencia(models.Model):
    idasistencia=models.AutoField(primary_key=True)
    ESTADOS_ASISTENCIA = [
        ('  ', 'No se tomó asistencia'),
        ('A', 'Ausente'),
        ('P', 'Presente'),
    ]
    estado = models.CharField(
        max_length=10,
        choices=ESTADOS_ASISTENCIA,
        default='NO_TOMADA'
    )
    fechaclase = models.DateField()
    tutor=models.ForeignKey(Tutor, on_delete=models.SET_NULL, null=True)
    estudiante=models.ForeignKey(Estudiante, on_delete=models.SET_NULL, null=True)
    aula = models.ForeignKey(Aula, on_delete=models.SET_NULL, null=True, blank=True)
    profesor_asistencia = models.BooleanField(default=False) # Campo para la asistencia del profesor
    
    def __str__(self):
        return f"{self.estudiante} - {self.fechaclase} - {self.get_estado_display()}"

class horario(models.Model):
    idhorario = models.AutoField(primary_key=True)
    fechainicio=models.CharField()
    fechafin=models.CharField()
    hora_inicio = models.TimeField()  
    hora_fin = models.TimeField()  
    diainicial = models.CharField(max_length=2)  
    diainicial_text = models.CharField()  
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE) 
    profesor = models.ForeignKey(Tutor, on_delete=models.CASCADE) 

    def __str__(self):
        return f"{self.profesor} - {self.diainicial} to {self.diafinal} - {self.hora_inicio} to {self.hora_fin}"

    class Meta:
        unique_together = ('profesor', 'hora_inicio', 'hora_fin', 'diainicial')  # Restricción única para evitar solapamiento de horarios

class year_electivo(models.Model):
    idyear=models.AutoField(primary_key=True)
    year=models.FloatField()
    fechainicio=models.DateField()
    fechafin=models.DateField()
    numsemana=models.FloatField()





