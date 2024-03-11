from drf_yasg import openapi
from drf_yasg.views import get_schema_view


def swagger():
    return get_schema_view(
        openapi.Info(
            title="Swagger",
            default_version='v1',
            description="API Documentation",
            license=openapi.License(name="Test License"),
        ),
        public=True,
        # permission_classes=[permissions.IsAuthenticated, ],
    )
