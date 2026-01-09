from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from base.api_views import CategoryApiView, BlogApiView, CommentApiView, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from base.api_views import ApiLogoutView

urlpatterns = [
    # JWT Authentication
    path('register/', RegisterView.as_view(), name='api_register'),
    path('login/', TokenObtainPairView.as_view(), name='api_login'),
    path('logout/', ApiLogoutView.as_view(), name='api_logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Categories
    path('categories/', CategoryApiView.as_view({'get': 'list', 'post': 'create'})),
    path('categories/<int:pk>/', CategoryApiView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # Blogs
    path('blogs/', BlogApiView.as_view({'get': 'list', 'post': 'create'})),
    path('blogs/<int:pk>/', BlogApiView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # Comments
    path('comments/', CommentApiView.as_view({'get': 'list', 'post': 'create'})),
    path('comments/<int:pk>/', CommentApiView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]
