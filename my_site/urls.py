from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from blog.views import QuestionViewSet, TagViewSet, CommentViewSet, signup
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
      path('auth/', include('rest_framework.urls', namespace='rest_framework')),  # SB-auth  # noqa
      path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # noqa
      path('signup/', signup, name='signup'),

      # path('api/auth/', include('djoser.urls')),  # token-authentication with djoser  # noqa
      # re_path(r'^auth/', include('djoser.urls.authtoken')), # token-authentication with djoser  # noqa
      # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT-authentication  # noqa
      # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT-authentication  # noqa
      # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # JWT-authentication  # noqa

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # noqa
