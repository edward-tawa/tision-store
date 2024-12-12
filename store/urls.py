"""
URL configuration for store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rest_framework import permissions
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


api_info = openapi.Info(
        title="e-store",
        default_version="v1",
        description="API description",
        terms_of_service = "",
        contact=openapi.Contact(email="tagumatawa@gmail.com"),
        license=openapi.License(name="MIT License"),
    )

schema_view = get_schema_view(
    api_info,
    public = True,
    permission_classes = [permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('store/', include('carstore.urls.store_urls')),
    path('store/api/schema/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-ui"),
    path('store/api/schema/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name="redoc-ui"),
    path('store/user/', include('carstore.urls.user_urls')),
    path('store/user/orders/', include('carstore.urls.order_urls')),
    path('store/customer/', include('carstore.urls.customer_urls')),
    path('store/products/', include('carstore.urls.product_urls')),
    path('store/categories/', include('carstore.urls.category_urls')),
]
