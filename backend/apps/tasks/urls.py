from rest_framework.routers import DefaultRouter
from .viewsets import TaskViewSet, TagViewSet

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")
router.register(r"tags", TagViewSet, basename="tag")

urlpatterns = router.urls
