from django.contrib import admin
from django.urls import path
from base.api_views import CategoryApiView, BlogApiView, CommentApiView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('categories/', CategoryApiView.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('categories/<int:pk>/', CategoryApiView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),

    path('blogs/', BlogApiView.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('blogs/<int:pk>/', BlogApiView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),

    path('comments/', CommentApiView.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('comments/<int:pk>/', CommentApiView.as_view({
        'delete': 'destroy'
    })),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

