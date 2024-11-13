from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Administrador, Persona, Tutor
from .serializers import AdminSerializer, PersonaSerializer, TutorSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdminSerializer

    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'cedula': openapi.Schema(type=openapi.TYPE_STRING, description='Cédula'),
                'primer_nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Primer nombre'),
                'segundo_nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Segundo nombre'),
                'primer_apellido': openapi.Schema(type=openapi.TYPE_STRING, description='Primer apellido'),
                'segundo_apellido': openapi.Schema(type=openapi.TYPE_STRING, description='Segundo apellido'),
                'genero': openapi.Schema(type=openapi.TYPE_STRING, description='Género'),
                'fecha_nacimiento': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha de nacimiento'),
                'estrato': openapi.Schema(type=openapi.TYPE_STRING, description='Estrato'),
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo electrónico'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña'),
            },
            required=['primer_nombre', 'primer_apellido', 'genero', 'fecha_nacimiento', 'estrato', 'correo', 'password'],
        ),
        responses={201: AdminSerializer, 400: 'Bad Request'}
    )
    @action(detail=False, methods=['post'])
    def create_admin(self, request):
        cedula = request.data.get("cedula")
        persona = Persona.objects.filter(cedula=cedula).first()
        if not persona:   
            persona_data = {
                "cedula": cedula,
                "primer_nombre": request.data.get("primer_nombre"),
                "segundo_nombre": request.data.get("segundo_nombre"),
                "primer_apellido": request.data.get("primer_apellido"),
                "segundo_apellido": request.data.get("segundo_apellido"),
                "genero": request.data.get("genero"),
                "fecha_nacimiento": request.data.get("fecha_nacimiento"),
                "estrato": request.data.get("estrato"),
                "password": request.data.get("password")
            }
        
       
            persona_serializer = PersonaSerializer(data=persona_data)
        
            if persona_serializer.is_valid():
                persona = persona_serializer.save()
                persona.set_password(persona_data['password']) 
                persona.save()
            else:
                return Response(persona_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            pass   
            
        admin_data = {  
            "correo": request.data.get("correo"),
            "persona": persona.id
                }
        admin_serializer = AdminSerializer(data=admin_data)
            
        if admin_serializer.is_valid():
            admin_serializer.save()
            return Response(admin_serializer.data, status=status.HTTP_201_CREATED)
        else:
            if not persona:
                persona.delete()
            return Response(admin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer

    @swagger_auto_schema(
        method='get',
        manual_parameters=[
            openapi.Parameter('idtutor', openapi.IN_QUERY, description="ID del tutor", type=openapi.TYPE_INTEGER)
        ],
        responses={200: TutorSerializer, 404: 'Not Found'}
    )
    @action(detail=False, methods=['get'])
    def get_tutor_per_id(self, request):
        idtutor = request.query_params.get("idtutor")
        if idtutor is not None:
            try:
                tutor = Tutor.objects.get(idtutor=idtutor)
                tutor_serializer = TutorSerializer(tutor)
                return Response(tutor_serializer.data, status=status.HTTP_200_OK)
            except Tutor.DoesNotExist:
                return Response({"error": "Tutor not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "idtutor parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'cedula': openapi.Schema(type=openapi.TYPE_STRING, description='Cédula'),
                'primer_nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Primer nombre'),
                'segundo_nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Segundo nombre'),
                'primer_apellido': openapi.Schema(type=openapi.TYPE_STRING, description='Primer apellido'),
                'segundo_apellido': openapi.Schema(type=openapi.TYPE_STRING, description='Segundo apellido'),
                'genero': openapi.Schema(type=openapi.TYPE_STRING, description='Género'),
                'fecha_nacimiento': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha de nacimiento'),
                'estrato': openapi.Schema(type=openapi.TYPE_STRING, description='Estrato'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña'),
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo electrónico'),
                'telefono': openapi.Schema(type=openapi.TYPE_STRING, description='Teléfono'),
                'direccion': openapi.Schema(type=openapi.TYPE_STRING, description='Dirección'),
            },
            required=['cedula', 'primer_nombre', 'primer_apellido', 'genero', 'fecha_nacimiento', 'estrato', 'password', 'correo'],
        ),
        responses={201: TutorSerializer, 400: 'Bad Request'}
    )
    @action(detail=False, methods=['post'])
    def create_tutor(self, request):
        cedula = request.data.get("cedula")
        persona = Persona.objects.filter(cedula=cedula).first()
        if not persona:
            # Crear nueva persona
            persona_data = {
                "cedula": cedula,
                "primer_nombre": request.data.get("primer_nombre"),
                "segundo_nombre": request.data.get("segundo_nombre"),
                "primer_apellido": request.data.get("primer_apellido"),
                "segundo_apellido": request.data.get("segundo_apellido"),
                "genero": request.data.get("genero"),
                "fecha_nacimiento": request.data.get("fecha_nacimiento"),
                "estrato": request.data.get("estrato"),
                "password": request.data.get("password")
            }
            persona_serializer = PersonaSerializer(data=persona_data)
            if persona_serializer.is_valid():
                persona = persona_serializer.save()
                persona.set_password(persona_data['password'])
                persona.save()
            else:
                return Response(persona_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Opcional: Actualizar datos de la persona existente
            pass

        # Crear tutor asociado a la persona
        tutor_data = {
            "persona": persona.id,
            "correo": request.data.get("correo"),
            "telefono": request.data.get("telefono"),
            "direccion": request.data.get("direccion")
        }
        tutor_serializer = TutorSerializer(data=tutor_data)
        if tutor_serializer.is_valid():
            tutor_serializer.save()
            return Response(tutor_serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Si la creación del tutor falla, eliminar la persona creada
            if not persona:
                persona.delete()
            return Response(tutor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer