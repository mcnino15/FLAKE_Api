# Generated by Django 5.1.2 on 2024-11-13 20:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aula',
            fields=[
                ('idaula', models.AutoField(primary_key=True, serialize=False)),
                ('grado', models.CharField(max_length=60)),
                ('gradunum', models.FloatField()),
                ('grupo', models.FloatField()),
                ('jornada', models.CharField(choices=[('D', 'Día'), ('T', 'Tarde'), ('N', 'Noche'), ('U', 'Unica'), ('X', 'No definido')], default='D', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Instituciones',
            fields=[
                ('idinstitucion', models.AutoField(primary_key=True, serialize=False)),
                ('instnombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('barrio', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='year_electivo',
            fields=[
                ('idyear', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.FloatField()),
                ('fechainicio', models.DateField()),
                ('fechafin', models.DateField()),
                ('numsemana', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('idestudiante', models.AutoField(primary_key=True, serialize=False)),
                ('aula', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='FLAKE_Service.aula')),
                ('instituciones', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FLAKE_Service.instituciones')),
            ],
        ),
        migrations.CreateModel(
            name='horario',
            fields=[
                ('idhorario', models.AutoField(primary_key=True, serialize=False)),
                ('hora', models.TimeField()),
                ('diainicial', models.CharField(max_length=2)),
                ('diafinal', models.CharField(max_length=20)),
                ('aula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FLAKE_Service.aula')),
            ],
        ),
        migrations.AddField(
            model_name='aula',
            name='institucion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FLAKE_Service.instituciones'),
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('idtutor', models.AutoField(primary_key=True, serialize=False)),
                ('telefono', models.CharField(max_length=30)),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('direccion', models.CharField(max_length=90)),
                ('instituciones', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='FLAKE_Service.instituciones')),
            ],
        ),
        migrations.CreateModel(
            name='notas',
            fields=[
                ('idnota', models.AutoField(primary_key=True, serialize=False)),
                ('calificacion', models.FloatField()),
                ('tutor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='FLAKE_Service.tutor')),
            ],
        ),
        migrations.AddField(
            model_name='aula',
            name='tutor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='FLAKE_Service.tutor'),
        ),
        migrations.CreateModel(
            name='asistencia',
            fields=[
                ('idasistencia', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.CharField(choices=[('X', 'No se tomó asistencia'), ('A', 'No fue'), ('P', 'Sí fue')], default='NO_TOMADA', max_length=10)),
                ('fechaclase', models.DateField()),
                ('estudiante', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='FLAKE_Service.estudiante')),
                ('tutor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='FLAKE_Service.tutor')),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cedula', models.CharField(max_length=30, unique=True)),
                ('primer_nombre', models.CharField(max_length=30)),
                ('segundo_nombre', models.CharField(blank=True, max_length=30, null=True)),
                ('primer_apellido', models.CharField(max_length=30)),
                ('segundo_apellido', models.CharField(blank=True, max_length=30, null=True)),
                ('genero', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], max_length=10)),
                ('fecha_nacimiento', models.DateField()),
                ('estrato', models.CharField(max_length=5)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='Los grupos a los que pertenece este usuario.', related_name='persona_set', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Permisos específicos para este usuario.', related_name='persona_permissions_set', to='auth.permission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='tutor',
            name='persona',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tutor_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='estudiante',
            name='persona',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='estudiante_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('idadministrador', models.AutoField(primary_key=True, serialize=False)),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('persona', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='admin_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
