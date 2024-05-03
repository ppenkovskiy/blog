"""
URL configuration for my_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings

from blog.views import *
from rest_framework import routers
from django.urls import path, include
from django.contrib.auth import views as auth_views

router = routers.DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'tags', TagViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include("blog.urls")),
                  path('api/', include(router.urls)),
                  path('auth/', include('rest_framework.urls', namespace='rest_framework')),  # SB-auth
                  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
                  path('signup/', signup, name='signup'),

                  # path('api/auth/', include('djoser.urls')),  # token-authentication with djoser
                  # re_path(r'^auth/', include('djoser.urls.authtoken')), # token-authentication with djoser
                  # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT-authentication
                  # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT-authentication
                  # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # JWT-authentication

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
