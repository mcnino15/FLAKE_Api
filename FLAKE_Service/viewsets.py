from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Administrador, Persona, Tutor, horario, Aula, Instituciones, asistencia, Estudiante, Notas
from .serializers import AdminSerializer, PersonaSerializer, TutorDetailSerializer,TutorCreateSerializer,EstudianteCreateSerializer, EstudianteDetailSerializer,HorarioSerializer, AulaSerializer, InstitucionSerializer, AsistenciaSerializer, TutorAsistenciaSerializer, fullnameEstudianteSerializer,NotasSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from datetime import datetime
from django.db import transaction

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
    def get_serializer_class(self):
        
        if self.action == 'create' or self.action == 'creartutor':
            return TutorCreateSerializer
        elif self.action == 'retrieve' or self.action == 'get_tutor_por_persona':
            return TutorDetailSerializer
        return TutorCreateSerializer

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
                'instituciones': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la institución'),
                'aula': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del aula'),
                'telefono': openapi.Schema(type=openapi.TYPE_STRING, description='Teléfono'),
                'direccion': openapi.Schema(type=openapi.TYPE_STRING, description='Dirección'),
            },
            required=['primer_nombre', 'primer_apellido', 'genero', 'fecha_nacimiento', 'estrato', 'correo', 'cedula', 'instituciones', 'aula','telefono','direccion'],
        ),
        responses={201: TutorDetailSerializer, 400: 'Bad Request'}
    )
    @action(detail=False, methods=['post'], url_path='creartutor')
    def crear_tutor(self, request):
        # Lógica de creación del tutor
        persona_data = {
            "cedula": request.data.get("cedula"),
            "primer_nombre": request.data.get("primer_nombre"),
            "segundo_nombre": request.data.get("segundo_nombre"),
            "primer_apellido": request.data.get("primer_apellido"),
            "segundo_apellido": request.data.get("segundo_apellido"),
            "genero": request.data.get("genero"),
            "fecha_nacimiento": request.data.get("fecha_nacimiento"),
            "estrato": request.data.get("estrato"),
            "correo": request.data.get("correo"),
            "password": request.data.get("password"),
        }
        
        persona_serializer = PersonaSerializer(data=persona_data)
        if persona_serializer.is_valid():
            persona = persona_serializer.save()
            persona.set_password(persona_data['password'])
        else:
            return Response(persona_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Validación para los campos 'telefono' y 'direccion'
        telefono = request.data.get("telefono")
        direccion = request.data.get("direccion")
        
        if not telefono or not direccion:
            return Response({"error": "Telefono y direccion son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        # Datos del tutor
        tutor_data = {
            "telefono": telefono,
            "direccion": direccion,
            "persona": persona.id,
            "correo": request.data.get("correo"),
            "instituciones": request.data.get("instituciones"),  # Asegúrate de pasar solo el ID
            "aula": request.data.get("aula"),
            
        }

        tutor_serializer = TutorCreateSerializer(data=tutor_data)
        if tutor_serializer.is_valid():
            tutor_serializer.save()
            return Response(tutor_serializer.data, status=status.HTTP_201_CREATED)
        else:
            persona.delete()  # Rollback persona creation if tutor creation fails
            return Response(tutor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['get'], url_path='detalle')
    def get_tutor_por_persona(self, request, pk=None):
        try:
            persona = Persona.objects.get(pk=pk)
            tutor = Tutor.objects.get(persona=persona)
            serializer = TutorDetailSerializer(tutor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Persona.DoesNotExist:
            return Response({"error": "Persona no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except Tutor.DoesNotExist:
            return Response({"error": "Estudiante no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
    


class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'crearestudiante':
            return EstudianteCreateSerializer
        elif self.action == 'retrieve' or self.action == 'get_estudiante_por_persona':
            return EstudianteDetailSerializer
        return EstudianteCreateSerializer

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
                'instituciones': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la institución'),
                'aula': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del aula'),
            },
            required=['primer_nombre', 'primer_apellido', 'genero', 'fecha_nacimiento', 'estrato', 'correo', 'cedula', 'instituciones', 'aula'],
        ),
        responses={201: EstudianteDetailSerializer, 400: 'Bad Request'}
    )
    @action(detail=False, methods=['post'], url_path='crearestudiante')
    def crear_estudiante(self, request):
        persona_data = {
            "cedula": request.data.get("cedula"),
            "primer_nombre": request.data.get("primer_nombre"),
            "segundo_nombre": request.data.get("segundo_nombre"),
            "primer_apellido": request.data.get("primer_apellido"),
            "segundo_apellido": request.data.get("segundo_apellido"),
            "genero": request.data.get("genero"),
            "fecha_nacimiento": request.data.get("fecha_nacimiento"),
            "estrato": request.data.get("estrato"),
            "password": request.data.get("password"),
        }
        
        persona_serializer = PersonaSerializer(data=persona_data)
        if persona_serializer.is_valid():
            persona = persona_serializer.save()
            persona.set_password(persona_data['password'])
            persona.save()
        else:
            return Response(persona_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        estudiante_data = {
            "persona": persona.id,
            "instituciones": request.data.get("instituciones"),
            "aula": request.data.get("aula"),
        }

        estudiante_serializer = EstudianteCreateSerializer(data=estudiante_data)
        if estudiante_serializer.is_valid():
            estudiante_serializer.save()
            return Response(estudiante_serializer.data, status=status.HTTP_201_CREATED)
        else:
            persona.delete()
            return Response(estudiante_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='detalle')
    def get_estudiante_por_persona(self, request, pk=None):
        try:
            persona = Persona.objects.get(pk=pk)
            estudiante = Estudiante.objects.get(persona=persona)
            serializer = EstudianteDetailSerializer(estudiante)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Persona.DoesNotExist:
            return Response({"error": "Persona no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except Estudiante.DoesNotExist:
            return Response({"error": "Estudiante no encontrado"}, status=status.HTTP_404_NOT_FOUND)





class NotasViewSet(viewsets.ModelViewSet):
    queryset = Notas.objects.all()
    serializer_class = NotasSerializer

    @action(detail=False, methods=['post'], url_path='registrar-notas')
    def registrar_notas(self, request):
        """
        Permite que un tutor registre o actualice las notas de un estudiante.
        """
        tutor_id = request.data.get('tutor')
        estudiante_id = request.data.get('estudiante')
        aula_id = request.data.get('aula')
        bloque1 = request.data.get('bloque1')
        bloque2 = request.data.get('bloque2')
        bloque3 = request.data.get('bloque3')
        bloque4 = request.data.get('bloque4')

        # Validar que todos los datos requeridos estén presentes
        if not all([tutor_id, estudiante_id, aula_id]):
            return Response(
                {"error": "Los campos tutor_id, estudiante_id y aula_id son obligatorios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Verificar que el tutor exista
            tutor = Tutor.objects.get(idtutor=tutor_id)

            # Verificar que el estudiante exista
            estudiante = Estudiante.objects.get(idestudiante=estudiante_id)

            # Verificar que el aula sea válida y que el tutor esté asignado a ella
            if tutor.aula.idaula != int(aula_id):
                return Response(
                    {"error": "El tutor no está asignado al aula proporcionada."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Crear o actualizar las notas
            notas, created = Notas.objects.get_or_create(
                estudiante=estudiante,
                aula_id=aula_id,
                tutor=tutor,
                defaults={
                    "bloque1": bloque1,
                    "bloque2": bloque2,
                    "bloque3": bloque3,
                    "bloque4": bloque4,
                },
            )

            # Actualizar si ya existe
            if not created:
                if bloque1 is not None:
                    notas.bloque1 = bloque1
                if bloque2 is not None:
                    notas.bloque2 = bloque2
                if bloque3 is not None:
                    notas.bloque3 = bloque3
                if bloque4 is not None:
                    notas.bloque4 = bloque4
                notas.calcular_calificacion_final()
                notas.save()

            serializer = NotasSerializer(notas)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Tutor.DoesNotExist:
            return Response({"error": "El tutor no existe."}, status=status.HTTP_404_NOT_FOUND)
        except Estudiante.DoesNotExist:
            return Response({"error": "El estudiante no existe."}, status=status.HTTP_404_NOT_FOUND)


class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


#NUEVOOOOOO    
class HorarioViewSet(viewsets.ModelViewSet):
    queryset = horario.objects.all()
    serializer_class = HorarioSerializer

    @action(detail=False, methods=['post'])
    def crear_horario_con_profesor(self, request):
        data = request.data
        profesor_id = data.get("profesor")
        fecha_inicio=data.get("fechainicio")
        fecha_final=data.get("fechafin")
        hora_inicio_str = data.get("hora_inicio")  
        hora_fin_str = data.get("hora_fin") 
        dia_inicial = data.get("diainicial") 
        dia_inicial_text = data.get("diainicial_text") 
        

        try:
            profesor = Tutor.objects.get(idtutor=profesor_id)  
        except Tutor.DoesNotExist:
            return Response({"error": "El profesor no existe."}, status=status.HTTP_404_NOT_FOUND)

        
        try:
            hora_inicio = datetime.strptime(hora_inicio_str, '%H:%M').time()
            hora_fin = datetime.strptime(hora_fin_str, '%H:%M').time()
        except ValueError:
            return Response({"error": "El formato de la hora es inválido. Usa 'HH:MM'."}, status=status.HTTP_400_BAD_REQUEST)


        horarios_existentes = horario.objects.filter(
            profesor=profesor,
            hora_inicio__lt=hora_fin,  
            hora_fin__gt=hora_inicio  
        )

        if horarios_existentes.exists():
            return Response(
                {"error": "El profesor ya tiene una clase en esta franja horaria."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save(profesor=profesor)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#NUEVOOO
class AulaViewSet(viewsets.ModelViewSet):
    queryset = Aula.objects.all()
    serializer_class = AulaSerializer
    
    @action(detail=False, methods=['post'])
    def crear_aula(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'], url_path='lista-estudiantes')
    def lista_estudiantes(self, request, pk=None):
        aula = self.get_object()
        estudiantes = aula.estudiantes.all()
        serializer = fullnameEstudianteSerializer(estudiantes, many=true)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
#NUEVOOOOO
class InstitucionViewSet(viewsets.ModelViewSet):
    queryset = Instituciones.objects.all()
    serializer_class = InstitucionSerializer
    
    @action(detail=False, methods=['post'])
    def create_institucion(self, request):
        serializer = InstitucionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = asistencia.objects.all()
    serializer_class = AsistenciaSerializer

    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'aula_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del aula'),
                'fechaclase': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha de la clase'),
                'asistencias': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'estudiante_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del estudiante'),
                            'estado': openapi.Schema(type=openapi.TYPE_STRING, description='Estado de asistencia ("O", "A", "X")')
                        },
                        required=['estudiante_id', 'estado']
                    ),
                    description='Lista de asistencias de estudiantes'
                )
            },
            required=['aula_id', 'fechaclase', 'asistencias']
        ),
        responses={200: 'Asistencias registradas exitosamente', 400: 'Bad Request'}
    )
    @action(detail=False, methods=['post'], url_path='tomar-asistencia')
    def tomar_asistencia(self, request):
        aula_id = request.data.get('aula_id')
        fechaclase = request.data.get('fechaclase')
        asistencias_data = request.data.get('asistencias', [])

        # Procesar las asistencias
        errores = []
        for asistencia_item in asistencias_data:
            estudiante_id = asistencia_item.get('estudiante_id')
            estado = asistencia_item.get('estado', ' ')

            # Asumimos que el estudiante ya pertenece al aula
            try:
                estudiante = Estudiante.objects.get(id=estudiante_id)
            except Estudiante.DoesNotExist:
                errores.append({'estudiante_id': estudiante_id, 'error': 'Estudiante no encontrado.'})
                continue

            # Registrar o actualizar la asistencia
            asistencia_obj, created = asistencia.objects.update_or_create(
                estudiante=estudiante,
                fechaclase=fechaclase,
                defaults={
                    'estado': estado,
                }
            )

        # Responder con los errores si los hubo
        if errores:
            return Response({'errores': errores}, status=status.HTTP_207_MULTI_STATUS)

        return Response({'mensaje': 'Asistencias registradas exitosamente.'}, status=status.HTTP_200_OK)
  
class AsistenciaTutorViewSet(viewsets.ModelViewSet):
    queryset = asistencia.objects.all()
    serializer_class = TutorAsistenciaSerializer

    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'fechaclase': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha de la clase'),
                'tutor_asistencia': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Asistencia del profesor (true para presente, false para ausente)'),
            },
            required=['fechaclase', 'tutor_asistencia']
        ),
        responses={200: 'Asistencia del tutor registrada exitosamente', 400: 'Bad Request'}
    )
    @action(detail=False, methods=['post'], url_path='tomar-asistencia-profesor')
    def tomar_asistencia_profesor(self, request):
        fechaclase = request.data.get('fechaclase')
        tutor_asistencia = request.data.get('tutor_asistencia')
        tutor= request.data.get('tutor')
        asistencia_obj, created = asistencia.objects.update_or_create(
            fechaclase=fechaclase,
            tutor=tutor,
            defaults={
                'profesor_asistencia': tutor_asistencia,
            }
        )
        serializer = TutorAsistenciaSerializer(asistencia_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
