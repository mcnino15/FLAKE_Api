from rest_framework.routers import DefaultRouter
from .viewsets import AdminViewSet, TutorViewSet,EstudianteViewSet,PersonaViewSet, HorarioViewSet, AulaViewSet, InstitucionViewSet, AsistenciaViewSet,NotasViewSet,AsistenciaTutorViewSet

router = DefaultRouter()
router.register(r'administradores', AdminViewSet)
router.register(r'tutores', TutorViewSet)
router.register(r'estudiantes', EstudianteViewSet)
router.register(r'personas', PersonaViewSet)
router.register(r'horarios', HorarioViewSet)
router.register(r'aulas', AulaViewSet)
router.register(r'instituciones', InstitucionViewSet)
router.register(r'asistencia', AsistenciaViewSet)
router.register(r'asistencia-tutor', AsistenciaTutorViewSet, basename='asistencia-tutor')
router.register(r'notas', NotasViewSet)