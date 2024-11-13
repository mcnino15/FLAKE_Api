
from rest_framework.routers import DefaultRouter
from .viewsets import AdminViewSet, TutorViewSet, PersonaViewSet

router = DefaultRouter()
router.register(r'administradores', AdminViewSet)
router.register(r'tutores', TutorViewSet)
router.register(r'personas', PersonaViewSet)
