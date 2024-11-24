from .models import Tutor ,Administrador, Persona, horario, Aula, Instituciones, asistencia, Estudiante, Notas,AsistenciaTutor
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = '__all__'
class PersonaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Persona
        fields = '__all__'
class TutorCreateSerializer(serializers.ModelSerializer):
    persona = serializers.PrimaryKeyRelatedField(queryset=Persona.objects.all())
    class Meta:
        model = Tutor
        fields = '__all__'

class TutorDetailSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer(read_only=True)

    class Meta:
        model = Tutor
        fields = '__all__'
        
class EstudianteCreateSerializer(serializers.ModelSerializer):
    persona = serializers.PrimaryKeyRelatedField(queryset=Persona.objects.all())

    class Meta:
        model = Estudiante
        fields = '__all__'





class LoginSerializer(serializers.Serializer):
    cedula = serializers.CharField()
    password = serializers.CharField(write_only=True)
   

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Añadir información adicional al token
        try:
            if hasattr(user, 'tutor_profile'):
                token['role'] = 'tutor'
                token['idtutor'] = user.tutor_profile.idtutor
            elif hasattr(user, 'admin_profile'):
                token['role'] = 'administrador'
                token['idadministrador'] = user.admin_profile.idadministrador
            else:
                token['role'] = 'unknown'
        except Persona.DoesNotExist:
            token['role'] = 'unknown'

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['role'] = refresh['role']
        
        if 'idtutor' in refresh:
            data['idtutor'] = refresh['idtutor']
        if 'idadministrador' in refresh:
            data['idadministrador'] = refresh['idadministrador']
        
        return data



class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = horario
        fields = '__all__'
#NUEVOOO
class AulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aula
        fields = '__all__' 
#NUEVOOOO        
class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instituciones
        fields = '__all__'
        
class EstudianteDetailSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer()
    instituciones=InstitucionSerializer()
    aula= AulaSerializer()

    class Meta:
        model = Estudiante
        fields = '__all__'
        
class EstudianteUpdateSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer()
    instituciones = serializers.PrimaryKeyRelatedField(queryset=Instituciones.objects.all())
    aula = serializers.PrimaryKeyRelatedField(queryset=Aula.objects.all())

    class Meta:
        model = Estudiante
        fields = '__all__'


class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = asistencia
        fields = '__all__'

class AsistenciaTutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsistenciaTutor
        fields = ['id', 'tutor', 'aula', 'fecha_asistencia', 'hora_inicio']

class fullnameEstudianteSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()
    class Meta:
        model = Estudiante
        fields = ['nombre_completo']
    def get_nombre_completo(self,obj):
        return f"{obj.primer_nombre} {obj.segundo_nombre or ''} {obj.primer_apellido} {obj.segundo_apellido or ''}".strip()
    


        
class NotasSerializer(serializers.ModelSerializer):
    # Incluye información adicional si necesitas mostrar datos de relaciones
    estudiante_nombre_completo = serializers.SerializerMethodField()
    aula_nombre = serializers.CharField(source='aula.nombre', read_only=True)  # Si Aula tiene un campo `nombre`
    tutor_nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = Notas
        fields = [
            'idnota',
            'estudiante',
            'estudiante_nombre_completo',
            'bloque1',
            'bloque2',
            'bloque3',
            'bloque4',
            'calificacion_final',
            'aula',
            'aula_nombre',
            'tutor',
            'tutor_nombre_completo'
        ]
        read_only_fields = ['calificacion_final']  # La calificación final se calcula automáticamente

    def get_estudiante_nombre_completo(self, obj):
        # Genera el nombre completo del estudiante
        return f"{obj.estudiante.persona.primer_nombre} {obj.estudiante.persona.primer_apellido}"

    def get_tutor_nombre_completo(self, obj):
        # Genera el nombre completo del tutor
        return f"{obj.tutor.persona.primer_nombre} {obj.tutor.persona.primer_apellido}"