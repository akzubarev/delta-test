from rest_framework.routers import DefaultRouter

from .views import ParcelsViewSet

router = DefaultRouter()
router.register("parcels", ParcelsViewSet)

urlpatterns = [
    *router.urls
]
