from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Ecommerce Assessment API",
        default_version='v1',
        description="API endpoints for Ecommerce. Find all information related to the routes under this document."
                    "\n\nThe `swagger-ui` view can be found [here](/)."
                    "\n\nThe `ReDoc` view can be found [here](/redoc/). ",
        terms_of_service="/docs/",
        contact=openapi.Contact(email="mwicwiribonface21@gmail.com"),
        license=openapi.License(name="Name License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('/api/v1/', include('djoser.urls')),
    path('/api/v1/', include('djoser.urls.jwt')),
    path('/api/v1/', include('store.api.urls')),

    # SWAGGER UI patterns
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
