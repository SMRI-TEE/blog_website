"""
URL configuration for blogmain project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from base import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('category/<int:id>/',views.posts_by_category,name='posts_by_category'),
    path('blogs/search/',views.search,name='search'),
    path('blogs/<slug:slug>/',views.blogs,name='blogs'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    
    # for categories crud 
    path('categories/',views.category_view,name='categories'),
    path('categories/add/',views.add_categories,name='add_categories'),
    path('categories/edit/<int:pk>/',views.edit_categories,name='edit_categories'),
    path('categories/delete/<int:pk>/',views.delete_categories,name='delete_categories'),
       
]+ static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)+ static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
