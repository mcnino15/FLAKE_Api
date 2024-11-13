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
    
class Tutor(models.Model):
    idtutor = models.AutoField(primary_key=True)
    telefono = models.CharField(max_length=30)
    correo = models.EmailField(unique=True)
    direccion = models.CharField(max_length=90)
    
    
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name='tutor_profile')

    # Relación con Instituciones
    instituciones = models.ForeignKey(Instituciones, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Tutor: {self.persona.primer_nombre} {self.persona.primer_apellido}"

class Administrador(models.Model):
    idadministrador = models.AutoField(primary_key=True)
    correo = models.EmailField(unique=True)
    
    # Relación uno a uno con Persona
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name='admin_profile')

    def __str__(self):
        return f"Administrador: {self.persona.primer_nombre} {self.persona.primer_apellido}"

class Aula(models.Model):
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
    institucion=models.ForeignKey(Instituciones, on_delete=models.CASCADE)
    tutor=models.ForeignKey(Tutor,  on_delete=models.SET_NULL, null=True)


class Estudiante(models.Model):
    idestudiante = models.AutoField(primary_key=True)
    instituciones = models.ForeignKey(Instituciones, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.SET_NULL, null=True, blank=True)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name='estudiante_profile')
    def __str__(self):
        return f"Estudiante: {self.persona.primer_nombre} {self.persona.primer_apellido}"


class notas(models.Model):
    idnota=models.AutoField(primary_key=True)
    calificacion=models.FloatField()
    tutor=models.ForeignKey(Tutor, on_delete=models.SET_NULL, null=True)

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
    tutor=models.ForeignKey(Tutor, on_delete=models.SET_NULL, null=True)
    estudiante=models.ForeignKey(Estudiante, on_delete=models.SET_NULL, null=True)

class horario(models.Model):
    idhorario=models.AutoField(primary_key=True)
    hora=models.TimeField()
    diainicial=models.CharField(max_length=2)
    diafinal=models.CharField(max_length=20)
    aula=models.ForeignKey(Aula, on_delete=models.CASCADE)

class year_electivo(models.Model):
    idyear=models.AutoField(primary_key=True)
    year=models.FloatField()
    fechainicio=models.DateField()
    fechafin=models.DateField()
    numsemana=models.FloatField()





